import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from horizon import messages
from horizon import exceptions

from .models import Installer
import plugins.api.razor as razor_api

LOG = logging.getLogger(__name__)


class CreateForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length="255", label=_("Installer Name"))
    os = forms.CharField(max_length="255", label=_("OS"))
    os_version = forms.CharField(max_length="255", label=_("OS Version"))
    description = forms.CharField(max_length="255", label=_("Description"),widget=forms.Textarea(
                       attrs={'style': 'height: 100px;'}))

    boot_seq_hidden = forms.CharField(required=False,widget=forms.HiddenInput())
    template_hidden = forms.CharField(required=False,widget=forms.HiddenInput())
    
    failure_url = 'horizon:plugins:installers:index'
	
    def __init__(self, request, *args, **kwargs):
        super(CreateForm, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            installer = razor_api.create_installer(Installer(data["name"], data["os"],data["os_version"],data["description"],data["boot_seq_hidden"],data["template_hidden"]))
            if installer["details"] == "":
                message = _('Installer %s was successfully created.') % data['name']                
                LOG.debug(message)
                messages.success(request, message)
            else:
                message = _('Failed to create %s. Details: %s') % (data['name'],installer['details'])
                LOG.debug(message)
                messages.error(request, message)

            return installer["name"]
        except Exception:
            msg = _('Failed to create installer "%s".') % data['name']
            LOG.info(msg)
            redirect = reverse(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)
            return False