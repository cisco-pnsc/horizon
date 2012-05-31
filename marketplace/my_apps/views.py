import logging

from django import http
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.views.generic import View, TemplateView
from django.utils.translation import ugettext as _

from horizon import views
from horizon import tables
from horizon import exceptions

from marketplace.applications import api as app_api

from .tables import MyApplicationsTable

LOG = logging.getLogger(__name__)

class IndexView(tables.DataTableView):
    table_class = MyApplicationsTable
    template_name = 'marketplace/my_apps/index.html'

    def get_data(self):
        try:
            apps = app_api.get_installed_applications(self.request)
        except:
            apps = []
            msg = _('Unable to retrieve installed application list.')
            exceptions.handle(self.request, msg)
        return apps
