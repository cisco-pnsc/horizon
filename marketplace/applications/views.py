import logging

from horizon import views
from horizon import api
from horizon import forms
from marketplace.applications import api as app_api

from .forms import StartApplication

LOG = logging.getLogger(__name__)

class IndexView(views.APIView):
    # A very simple class-based view...
    template_name = 'marketplace/applications/index.html'

    def get_data(self, request, context, *args, **kwargs):
        apps = app_api.get_all_applications(request)
        context['apps'] = apps
        return context

class DetailView(views.APIView):
    template_name = 'marketplace/applications/details.html'

    def get_data(self, request, context, *args, **kwargs):
        # Get application
        app = app_api.get_application(request, kwargs['app_id'])
        # Get all flavors
        flavor_list = api.flavor_list(request)
        flavors = {}
        for flavor in flavor_list:
            flavors[flavor.id] = flavor.name

        # Get application flavors
        app_flavor_list = app_api.get_application_flavors(request, kwargs['app_id'])
        app_flavors = []
        for flavor in app_flavor_list:
            app_flavors.append({
                'id': flavor.flavor_id,
                'recommended': flavor.recommended,
                'name': flavors[flavor.flavor_id]
            })

        # Get all versions of the application
        app_versions = app_api.get_application_versions(request, kwargs['app_id'])
        # Get security group list
        security_groups = api.security_group_list(request)
        # Get keypair list
        keypairs = api.keypair_list(request)

        context['app'] = app
        context['app_flavors'] = app_flavors
        context['app_versions'] = app_versions
        context['security_groups'] = security_groups
        context['keypairs'] = keypairs
        context['support_map'] = {
            'supported': 'Supported',
            'limited_support': 'Limited Support',
            'unsupported': 'Unsupported',
        }
        return context

class StartView(forms.ModalFormView):
    template_name = 'marketplace/applications/start.html'
    form_class = StartApplication

    def get_initial(self):
        # Get app name
        app = app_api.get_application(self.request, self.kwargs['app_id'])
        name = app.name
        return {
                'app_id': self.kwargs['app_id'],
                'name': name
                }
