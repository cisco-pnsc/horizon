import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from horizon import messages
from horizon import exceptions

import plugins.api.razor as razor_api

LOG = logging.getLogger(__name__)


class CreateForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length="255", label=_("Repository Name"))
    iso_url = forms.URLField(max_length="255", label=_("ISO Url"),help_text=_("An external (HTTP) URL to load "
                                            "the image from."))
    failure_url = 'horizon:plugins:repos:index'

    def __init__(self, request, *args, **kwargs):
        super(CreateForm, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            repo = razor_api.create_repo(data["name"], data["iso_url"])
            if repo["details"] == "":
	    	 message = _('Repository %s was successfully created.') % data['name']
            	 messages.success(request, message)
            else:
		 message = _('Failed to create %s. Details: %s') % (data['name'],repo['details'])
            	 messages.error(request, message)

            return repo["name"]
        except Exception:
            msg = _('Failed to create repo "%s".') % data['name']
            LOG.info(msg)
            redirect = reverse(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)
            return False
