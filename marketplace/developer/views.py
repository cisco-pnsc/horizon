import logging

from horizon import api
from horizon import forms
from horizon import tables

from .tables import DevAppsTable
from .forms import CreateApplication, CreateApplicationVersion

from marketplace.applications import api as app_api

LOG = logging.getLogger(__name__)

class IndexView(tables.DataTableView):
    table_class = DevAppsTable
    template_name = 'marketplace/developer/index.html'

    def get_data(self):
        dev_apps = app_api.get_dev_applications(self.request)
        return dev_apps

class CreateView(forms.ModalFormView):
    form_class = CreateApplication
    template_name = 'marketplace/developer/create.html'
    
    def get_initial(self):
        # Get all flavors
        flavors = api.flavor_list(self.request)
        # Get glance images
        images = api.image_list_detailed(self.request)
        return { 'flavors': flavors,
                 'images': images }

class CreateVersionView(forms.ModalFormView):
    form_class = CreateApplicationVersion
    template_name = 'marketplace/developer/create_version.html'

    def get_initial(self):
        # Get all flavors
        flavors = api.flavor_list(self.request)
        app_id =  self.kwargs['app_id']
        # Get app details
        app = app_api.get_application(self.request, app_id)
        
        # Get application flavors
        #app_flavors = app_api.get_application_flavors(self.request, app_id)

        # Get application versions
        app_versions = app_api.get_application_versions(self.request, app_id)

        return {
            'app': app,
            'flavors': flavors,
            'versions': app_versions
        }
