import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from horizon import messages
from horizon import exceptions

from .models import VLAN, MCPolicy

import plugins.api.ucs as ucs_api

LOG = logging.getLogger(__name__)

ADD_MCPOLICY_URL = "horizon:plugins:lan:vlans:create_mcpolicy"

class CreateForm(forms.SelfHandlingForm):
    configuration_choices = (('', 'Command/Global',), ('/A', 'FabricA',), ('/B', 'FabricB',), ('Both', 'Both Fabrics Configure Differently',))
    sharing_choices = (('none', 'None',), ('primary', 'Primary',), ('isolated', 'Isolated',))
    
    name = forms.CharField(max_length="255", label=_("Vlan Name"))
    multicast_policy = forms.DynamicChoiceField(label=_("Multicast Policy"),add_item_link=ADD_MCPOLICY_URL)
    configuration = forms.ChoiceField(label=_("Configuration") ,widget=forms.RadioSelect(attrs={'onclick': 'check_click();'}), initial = '',  choices = configuration_choices, required = False,)
    id = forms.CharField(max_length="255", label=_("Vlan ID"))
    sharing_type = forms.ChoiceField(widget=forms.RadioSelect,initial = 'none', choices = sharing_choices, required = False,)
    
    
    # --- display only if the user clicked on 'Both Fabrics Confiugre...'.
    # - these fields below are only for fabric b configuration.
    # - the previous fields are for fabric a configuration
    id_b = forms.CharField(max_length="255", label=_("Fabric B: Vlan ID"))
    sharing_type_b = forms.ChoiceField(widget=forms.RadioSelect(attrs={'style': 'display:"none"'}),initial = 'none', choices = sharing_choices, required = False,)
    
    failure_url = 'horizon:plugins:lan:index'

    def __init__(self, request, *args, **kwargs):
        super(CreateForm, self).__init__(request, *args, **kwargs)
        self.fields['multicast_policy'].choices = [('none','Not Set')] + [(mc_policy, mc_policy) for mc_policy in ucs_api.get_all_multicast_policies()]
     
    def handle(self, request, data):
        try:
            conf_arr = []
            conf_arr.append({'vlan_id' : data['id'] , 'sharing_type' : data['sharing_type'] ,'fabric' : data['configuration']})

            if data['configuration'] == 'Both':
                # change path to fabric
                conf_arr[0]['fabric'] = '/A'
                conf_arr.append({'vlan_id' : data['id_b'] , 'sharing_type' : data['sharing_type_b'] ,'fabric' : '/B'})

            if data['multicast_policy'] == 'none':
                data['multicast_policy'] = ''
                
            vlan = ucs_api.create_vlan(data['name'],data['multicast_policy'],conf_arr)
            if 'status' not in vlan:
                message = _('Vlan %s was successfully created.') % data['name']
                LOG.debug(message)
                messages.success(request, message)
            else:
                message = _('Failed to create Vlan %s. Details: %s.  %s') % (data['name'], vlan['errorCode'], vlan['errorDescr'])
                LOG.debug(message)
                messages.error(request, message)

            return VLAN(data['id'],data['name'])
        except Exception:
            msg = _('Failed to create Vlan "%s".') % data['name']
            LOG.info(msg)
            redirect = reverse(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)
            return False
        
        


class CreateMCPolicyForm(forms.SelfHandlingForm):
    state_choices = (('enabled', 'Enabled',), ('disabled', 'Disabled',),)
    
    name = forms.CharField(max_length="255", label=_("Multicast Policy Name"))
    icmp_snooping= forms.ChoiceField(label=_("ICMP Snooping State"),widget=forms.RadioSelect,initial = 'enabled', choices = state_choices)
    icmp_snooping_querier= forms.ChoiceField(label=_("ICMP Snooping Querier State"),widget=forms.RadioSelect,initial = 'disabled', choices = state_choices)
   
    failure_url = 'horizon:plugins:lan:vlans:create'

    def __init__(self, request, *args, **kwargs):
        super(CreateMCPolicyForm, self).__init__(request, *args, **kwargs)
      
    def handle(self, request, data):
        try:
            mcpolicy = ucs_api.create_multicast_policy(data['name'], data['icmp_snooping'], data['icmp_snooping_querier'])
            if 'status' not in mcpolicy:
                message = _('Multicast policy %s was successfully created.') % data['name']
                LOG.debug(message)
                messages.success(request, message)
            else:
                message = _('Failed to create multicast policy %s. Details: %s. %s') % (data['name'], mcpolicy['errorCode'], mcpolicy['errorDescr'])
                LOG.debug(message)
                messages.error(request, message)
                return None
            return MCPolicy(data['name'], data['icmp_snooping'], data['icmp_snooping_querier'])
        except Exception:
            msg = _('Failed to create multicast policy "%s".') % data['name']
            LOG.info(msg)
            redirect = reverse(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)
            return False
        