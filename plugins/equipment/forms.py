import logging
import ast

from django import shortcuts
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from horizon import messages
from horizon import exceptions

import plugins.api.ucs as ucs_api
import plugins.api.accessories as accessories

LOG = logging.getLogger(__name__)
      
class AssociateServiceProfileForm(forms.SelfHandlingForm):
    id = forms.CharField(label=_("Server ID"), required = False,
                                 widget=forms.TextInput(
                                     attrs={'readonly': 'readonly'}))
    name = forms.CharField(label=_("Server Name"), required = False,
                                 widget=forms.TextInput(
                                     attrs={'readonly': 'readonly'}))
    profile_name_prefix = forms.CharField(label=_("Profile Name Prefix"))
    templates = forms.ChoiceField(label=_("Service Profile Templates"))
    target_org = forms.ChoiceField(label=_("Target Organization"))
    
    failure_url = 'horizon:plugins:equipment:index'
    
    def __init__(self, request, *args, **kwargs):
        super(AssociateServiceProfileForm, self).__init__(request, *args, **kwargs)
        self.fields['name'].initial = kwargs
        self.fields['templates'].choices = [(template_details['name'], template_details['name']) for template,template_details in ucs_api.get_all_templates().items()]
        self.fields['target_org'].choices = [(org, org) for org in ucs_api.get_all_organizations()]
        

    def handle(self, request, data):
        try:
            result = ucs_api.associate_service_profile_from_template(data['templates'],data['profile_name_prefix'],data['target_org'],data['id'])
            if 'status' not in result:
                message = _('Profile %s was successfully assigned.') % data['profile_name_prefix']
                LOG.debug(message)
                messages.success(request, message)
            else:
                message = _('Failed to assign profile %s. Details: %s : %s') % (data['templates'],result['errorCode'],result['errorDescr'])
                LOG.debug(message)
                messages.error(request, message)
            return result
        except Exception:
            msg = _('Failed to assign profile %s.') % data['name']
            LOG.info(msg)
            redirect = reverse(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)

class DisassociateServiceProfileForm(forms.SelfHandlingForm):
    id = forms.CharField(label=_("Server ID"), required = False,
                                 widget=forms.TextInput(
                                     attrs={'readonly': 'readonly'}))
    name = forms.CharField(label=_("Server Name"), required = False,
                                 widget=forms.TextInput(
                                     attrs={'readonly': 'readonly'}))
    profile_name = forms.CharField(label=_("Profile Name"), required = False,
                                 widget=forms.TextInput(
                                     attrs={'readonly': 'readonly'}))
    
    failure_url = 'horizon:plugins:equipment:index'
    
    def __init__(self, request, *args, **kwargs):
        super(DisassociateServiceProfileForm, self).__init__(request, *args, **kwargs)
        self.fields['profile_name'].initial = kwargs

    def handle(self, request, data):
        try:
            if data['profile_name'] == 'Not Assigned':
               message = _('Server in not assigned to any profile')
               LOG.debug(message)
               messages.info(request, message)
            else: 
                result = ucs_api.disassociate_service_pofile_to_server(data['id'])
                if 'status' not in result:
                    message = _('Dissociate service profile %s successfully.') % data['name']
                    LOG.debug(message)
                    messages.success(request, message)
                else:
                    message = _('Failed to dissociate service profile %s. Details: %s : %s') % (data['profile_name'],result['errorCode'],result['errorDescr'])
                    LOG.debug(message)
                    messages.error(request, message)
                    return result
            return True
        except Exception:
            msg = _('Failed to dissociate service profile %s.') % data['name']
            LOG.info(msg)
            redirect = reverse(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)


class AssociateMultipleServiceProfilesForm(forms.SelfHandlingForm):

    templates = forms.ChoiceField(label=_("Service Profile Templates"))
    profile_name_prefix = forms.CharField(label=_("Profile Name Prefix"))
    target_org = forms.ChoiceField(label=_("Target Organization"))
    start_num = forms.IntegerField(label=_("Start Counting From"),required=False)
    servers_hidden = forms.CharField(required=False,widget=forms.HiddenInput())
    
    failure_url = 'horizon:plugins:equipment:index'
    
    def __init__(self, request, *args, **kwargs):
        super(AssociateMultipleServiceProfilesForm, self).__init__(request, *args, **kwargs) 
        self.fields['templates'].choices =  [(template_details['name'], template_details['name']) for template,template_details in ucs_api.get_all_templates().items()]
        self.fields['target_org'].choices = [(org, org) for org in ucs_api.get_all_organizations()]
         
    def handle(self, request, data):
        try:
            chosen_servers = accessories.convert(ast.literal_eval(data['servers_hidden']))
          
            if not data['start_num']:
                data['start_num'] = 0
                            
            result = ucs_api.associate_multiple_service_profiles_from_template(data['templates'],data['profile_name_prefix'], data['target_org'],data['start_num'],chosen_servers)
            
            if 'status' not in result:
                message = _('Profile %s was successfully assigned to servers: %s') % (data['templates'],result.keys())
                LOG.debug(message)
                messages.success(request, message)
            else:
                message = _('Failed to assign profile %s. Details: %s : %s') % (data['templates'],result['errorCode'],result['errorDescr'])
                LOG.debug(message)
                messages.error(request, message)
            return result
        except Exception:
            msg = _('Failed to assign profile %s to servers: %s') % (data['templates'],request.POST.getlist('servers'))
            LOG.info(msg)
            redirect = reverse(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)

class ShutdownServerForm(forms.SelfHandlingForm):
    name = forms.CharField(label=_("Server Name"), required = False,
                             widget=forms.TextInput(
                                 attrs={'readonly': 'readonly'}))
    hard_shutdown = forms.BooleanField(label=_("Hard Shutdown"),required=False)
    
    failure_url = 'horizon:plugins:equipment:index'
    
    def __init__(self, request, *args, **kwargs):
        super(ShutdownServerForm, self).__init__(request, *args, **kwargs)
        

    def handle(self, request, data):
        try:
            result = ucs_api.shutdown_server(data['name'],data['hard_shutdown'])
            if 'status' not in result:
                message = _('Shutdown server %s successfully.') % data['name']
                LOG.debug(message)
                messages.success(request, message)
            else:
                message = _('Failed to shutdown server %s. Details: %s : %s') % (data['name'],result['errorCode'],result['errorDescr'])
                LOG.debug(message)
                messages.error(request, message)
            return result
        except Exception:
            msg = _('Failed to shutdown server %s.') % data['name']
            LOG.info(msg)
            redirect = reverse(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)
            
class DownloadDataForm(forms.SelfHandlingForm):
   
    format_choices = [('csv','csv')]
    format = forms.ChoiceField(label=_("Export Format"), choices = format_choices)
    servers = forms.CharField(widget=forms.HiddenInput(),required = False)
    
    failure_url = 'horizon:plugins:equipment:index'
    
    def __init__(self, request, *args, **kwargs):
        super(DownloadDataForm, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            request.session['servers'] = ast.literal_eval(data['servers'])
            request.session['format'] = data['format']
            return shortcuts.redirect(reverse('horizon:plugins:equipment:download_data'))

        except Exception as e:
            LOG.exception("Exception in Download Data.csv.")
            messages.error(request, _('Error Downloading Data.csv: %s') % e)
            return shortcuts.redirect(reverse(self.failure_url)) 
    