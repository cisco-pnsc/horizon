import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from horizon import messages
from horizon import exceptions

from .models import Broker
import plugins.api.razor as razor_api

LOG = logging.getLogger(__name__)

class CreateForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length="255", label=_("Broker Name"))
    configuration_server = forms.CharField(max_length="255", required=False, label=_("Configuration Server"))
    configuration_version = forms.CharField(max_length="255", required=False, label=_("Configuration Version"))
    broker_type = forms.CharField(max_length="255", label=_("Broker Type"))

    failure_url = 'horizon:plugins:brokers:index'

    def __init__(self, request, *args, **kwargs):
        super(CreateForm, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
         broker = razor_api.create_broker(Broker(data["name"], data["configuration_server"], data["configuration_version"], data["broker_type"]))
            
         if broker["details"] == "":
             message = _('Broker %s was successfully created.') % data['name']
             LOG.debug(message)
             messages.success(request, message)
         else:
             message = _('Failed to create %s. Details: %s') % (data['name'], broker['details'])
             LOG.debug(message)
             messages.error(request, message)
         return broker["name"]
        except Exception:
            msg = _('Failed to create broker "%s".') % data['name']
            LOG.info(msg)
            redirect = reverse(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)
            return False
