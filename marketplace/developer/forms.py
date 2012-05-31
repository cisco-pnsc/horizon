import logging
import uuid

from datetime import datetime, timedelta

from django import shortcuts
from django.contrib import messages
from django.core import validators
from django.utils.translation import ugettext as _

from horizon import exceptions
from horizon import forms
from marketplace.applications import api as app_api

LOG = logging.getLogger(__name__)

class CreateApplication(forms.SelfHandlingForm):
    name = forms.CharField(max_length="128",
                           label=_("Application Name"),
                           required=True)
    icon = forms.ImageField(label=_("Application Icon"))
    version = forms.CharField(max_length="10",
                              label=_("Application Version"),
                               required=True)
    description = forms.CharField(widget=forms.widgets.Textarea(),
                                  label=_("Application Description"),
                                  required=True)
    support = forms.CharField(widget=forms.widgets.Textarea(),
                              label=_("Application Support"),
                              required=True)
    eula = forms.CharField(widget=forms.widgets.Textarea(),
                           label=_("Application EULA"),
                           required=True)
    base = forms.CharField(widget=forms.widgets.TextInput(),
                           label=_("Base Operating System"),
                           required=True)
    delivery = forms.CharField(widget=forms.widgets.TextInput(),
                               label=_("Application Delivery Method"),
                               required=True)
    image = forms.ChoiceField(widget=forms.widgets.Select(),
                              label=_("Select Glance Image"))
    flavors = forms.MultipleChoiceField(widget=forms.widgets.SelectMultiple(),
                                label=_("Select Allowed flavors"),
                                required=True)
    cost = forms.CharField(widget=forms.widgets.TextInput(),
                           label=_("Application Cost"),
                           required=True)
    recommended = forms.ChoiceField(widget=forms.widgets.Select(),
                                  label=_("Select Recommended flavor"))
    supported = forms.ChoiceField(widget=forms.widgets.Select(),
                                  label=_("Supported?"),
                                  choices=(
                                    ('S','Supported'),
                                    ('L','Limited Support'),
                                    ('U','Unsupported')
                                  ))
                                
                   
    def __init__(self, *args, **kwargs):
        super(CreateApplication, self).__init__(*args, **kwargs)
        initials = kwargs.get("initial", {})
        flavors = initials.get("flavors", [])
        images = initials.get("images", [])

        flavor_choices = []
        for flavor in flavors:
            flavor_choices.append((flavor.id, flavor.name))
       
        image_choices = []
        for image in images:
            image_choices.append((image.id, image.name))

        self.fields['flavors'].choices = flavor_choices
        self.fields['image'].choices = image_choices
        self.fields['recommended'].choices = flavor_choices

    def handle(self, request, data):
        try:
            file_contents = self.files['icon'].read()
            id = uuid.uuid4()
            app_api.create_application(
                request = request,
                id = id,
                name = data['name'],
                description = data['description'],
                eula = data['eula'],
                support = data['support'],
                icon = self.files['icon'],
                base = data['base'],
                delivery = data['delivery'],
                version = data['version'],
                flavors = data['flavors'],
                cost = data['cost'],
                supported = data['supported'],
                recommended = data['recommended'],
                image = data['image']
            )
            messages.success(request, _("Application created successfully."))
        except:
            exceptions.handle(request, _('Unable to create application.'))
        return shortcuts.redirect("horizon:marketplace:developer:index")

class CreateApplicationVersion(forms.SelfHandlingForm):
    id = forms.CharField(widget=forms.widgets.HiddenInput())
    supported = forms.ChoiceField(widget=forms.widgets.Select(),
                                  label=_("Supported?"),
                                  choices=(
                                    ('S','Supported'),
                                    ('L','Limited Support'),
                                    ('U','Unsupported')
                                  ))
    support = forms.CharField(widget=forms.widgets.Textarea(),
                              label=_("Application Support"),
                              required=True)
    version = forms.CharField(max_length="10",
                              label=_("Application Version"),
                              required=True)

    def __init__(self, *args, **kwargs):
        super(CreateApplicationVersion, self).__init__(*args, **kwargs)
        initials = kwargs.get("initial", {})

        app = initials.get("app")
        versions = initials.get("versions")
        images = initials.get("images", [])

        # Prepopulate form fields
        self.fields['id'].initial = app.id

        # Get the last version
        min_date = datetime.min
        for version in versions:
            if version.created_on > min_date:
                min_date = version.created_on
                latest_version = version
        self.fields['support'].initial = latest_version.support

        image_choices = []
        for image in images:
            image_choices.append((image.id, image.name))
    

    def handle(self, request, data):
        try:
            app_api.create_application_version(
                request = request,
                application_id = data['id'],
                version = data['version'],
                support = data['support'],
                supported = data['supported'],
                image = data['image']
            )
            messages.success(request, _("Application created successfully."))
        except:
            exceptions.handle(request, _('Unable to create application.'))
        return shortcuts.redirect("horizon:marketplace:developer:index")
