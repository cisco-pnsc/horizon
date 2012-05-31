import logging

from django import shortcuts
from django.core import urlresolvers
from django.utils.translation import ugettext as _

from horizon import tables
from horizon import exceptions

from marketplace.applications import api as app_api

LOG = logging.getLogger(__name__)

class CreateApplication(tables.LinkAction):
    name = "create"
    verbose_name = _("Create New Application")
    url = "horizon:marketplace:developer:create"
    classes = ("ajax-modal", "btn-create", "btn-success")

class CreateVersion(tables.LinkAction):
    name = "new_version"
    verbose_name = _("Create New Version")
    url = "horizon:marketplace:developer:create_version"
    classes = ("ajax-modal", "btn-create")

class DeleteApplication(tables.DeleteAction):
    data_type_singular = _("Application")
    data_type_plural = _("Applications")

    def delete(self, request, obj_id):
        app_api.delete_application(request, obj_id)

class DevAppsTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_('Id'))
    name = tables.Column('name', verbose_name=_('Name'))

    def get_object_id(self, app):
        return app.id
    
    class Meta:
        name = "dev_apps"
        verbose_name = _("List of applications you own")
        table_actions = (CreateApplication, DeleteApplication,)
        row_actions = (CreateVersion, DeleteApplication,)
