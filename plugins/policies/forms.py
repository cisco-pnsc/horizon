import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from horizon import messages
from horizon import exceptions

from .models import Policy
import plugins.api.razor as razor_api

LOG = logging.getLogger(__name__)

class CreateForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length="255", label=_("Policy Name"))
    repo_name = forms.ChoiceField(label=_("Repository Name"))
    installer_name = forms.CharField(max_length="255", label=_("Installer Name"))
    broker_name = forms.ChoiceField(label=_("Broker Name"))
    hostname = forms.CharField(max_length="255", label=_("Host Name"))
    root_password = forms.CharField(max_length="10",widget=forms.PasswordInput, label=_("Root Password"))
    max_count = forms.IntegerField(label=_("Max Count"))
    rule_number = forms.IntegerField(label=_("Rule Number"))
    enabled = forms.BooleanField(label=_("enabled"), required=False)
    tags = forms.CharField(required=False,widget=forms.HiddenInput())
    failure_url = 'horizon:plugins:policies:index'

    def __init__(self, request, *args, **kwargs):
        super(CreateForm, self).__init__(request, *args, **kwargs)
        self.fields['repo_name'].choices = [(repo, repo) for repo in razor_api.get_all_repos()]
        self.fields['broker_name'].choices = [(broker, broker) for broker in razor_api.get_all_brokers()]
           
    def handle(self, request, data):
        try:
	    if data['tags'] == '':
		message = _('Failed to create %s. Details: Same tag policy had been selcted twice') % data['name']
		messages.error(request, message)
		return True
	    #to cancel redirection just return False without any message. message can be added as an alert in _create.html js.
	    policy = razor_api.create_policy(Policy(data["name"],data["repo_name"],data["installer_name"],data["broker_name"],data["hostname"],data["root_password"],data["max_count"],data["rule_number"],data["tags"],data["enabled"]))
	    if policy["details"] == "":
		message = _('Policy %s was successfully created.') % data['name']
		messages.success(request, message)
	    else:
		message = _('Failed to create %s. Details: %s') % (data['name'], policy ['details'])
		messages.error(request, message)
	    return policy["name"]
        except Exception:
            msg = _('Failed to create policy "%s".') % data['name']
            LOG.info(msg)
            redirect = reverse(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)
            return False

     
 