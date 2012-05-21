import logging
import uuid

from django import shortcuts
from django.contrib import messages
from django.core import validators
from django.utils.translation import ugettext as _

from horizon import exceptions
from horizon import forms
from marketplace.applications import api as app_api

LOG = logging.getLogger(__name__)


class StartApplication(forms.SelfHandlingForm):
    iname = forms.CharField(max_length="128",
                            label=_("Instance Name"),
                            required=True)
    app_id = forms.CharField(widget=forms.widgets.HiddenInput())
    version = forms.CharField(widget=forms.widgets.HiddenInput())
    flavor = forms.CharField(widget=forms.widgets.HiddenInput())
    sec_grp = forms.CharField(widget=forms.widgets.HiddenInput())
    zone = forms.CharField(widget=forms.widgets.HiddenInput())
    keypair = forms.CharField(widget=forms.widgets.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(StartApplication, self).__init__(*args, **kwargs)
        self.fields['app_id'].value = kwargs['initial']['app_id']
        # Generate uuid for instance name
        uname = uuid.uuid4()
        self.fields['iname'].initial = kwargs['initial']['name'] +'--'+ uname.get_hex()

    def handle(self, request, data):
        name = data['iname']
        app_id = data['app_id']
        flavor = data['flavor']
        version = data['version']
        zone = data['zone']
        sec_grp = data['sec_grp']
        keypair = data['keypair']

        try:
            app_api.start_application(request, app_id, flavor, name,
                                      version, zone, sec_grp, keypair)
            messages.success(request, _("Application started successfully."))
        except:
            exceptions.handle(request, _('Unable to start application.'))
        return shortcuts.redirect("horizon:marketplace:applications:details", app_id)
