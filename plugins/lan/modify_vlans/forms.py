import logging
 
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from horizon import messages
from horizon import exceptions
 
import plugins.api.ucs as ucs_api
 
LOG = logging.getLogger(__name__)
 
ADD_VLAN_URL = "horizon:plugins:lan:vlans:create"
 
class AddVlanForm(forms.SelfHandlingForm):
    id = forms.CharField(required=False,widget=forms.HiddenInput())
    name = forms.CharField(max_length="255", label=_("Nic Name"), required = False,
                                 widget=forms.TextInput(
                                     attrs={'readonly': 'readonly'}))
  
    vlans_cb = forms.MultipleChoiceField(label=_("Vlans"),widget=forms.CheckboxSelectMultiple(), required = False,)
    native = forms.ChoiceField(label=_("Native Vlan"), widget = forms.Select(attrs={'onclick' : 'on_native_change()'}))
    
    failure_url = 'horizon:plugins:lan:index'
 
    def __init__(self, request, *args, **kwargs):
        super(AddVlanForm, self).__init__(request, *args, **kwargs)
        vlans = ucs_api.get_all_vlans().items()
        self.fields['vlans_cb'].choices = [(details['name'],details['name']) for vlan, details in vlans]
        if 'vlans' in kwargs['initial'] and 'default' in kwargs['initial']:
            self.fields['vlans_cb'].initial  = [vlan for vlan in kwargs['initial']['vlans']]
            self.fields['native'].choices = [('none', 'none')] + [(details['name'],details['name']) for vlan, details in vlans]
            self.fields['native'].initial = kwargs['initial']['default']
      
    def handle(self, request, data):
        try:
            new_vlans = request.POST.getlist('vlans_cb')
            result = ucs_api.add_vlan(data['id'],new_vlans,data['native'])
            if 'status' not in result:
                message = _('Modified Nic %s vlans successfully.') % (data['name'])
                LOG.debug(message)
                messages.success(request, message)
            else:
                message = _('Failed to modify vlans. Details: %s.  %s') % (result['errorCode'], result['errorDescr'])
                LOG.debug(message)
                messages.error(request, message)
 
            return result
        except Exception:
            msg = _('Failed to add vlan "%s".') % data['vlans_cb']
            LOG.info(msg)
            redirect = reverse(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)
 
