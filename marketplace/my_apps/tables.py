import logging

from django import shortcuts
from django.core import urlresolvers
from django.utils.translation import ugettext as _

from horizon import tables
from horizon import exceptions

from marketplace.applications import api as app_api

LOG = logging.getLogger(__name__)

def get_instance_link(datum):
    view = "horizon:nova:instances_and_volumes:instances:detail"
    if datum.instance_id:
        return urlresolvers.reverse(view, args=(datum.instance_id,))
    else:
        return None

class DeleteInstance(tables.DeleteAction):
    data_type_singular = _("Application")
    data_type_plural = _("Applications")

    def delete(self, request, obj_id):
        app_api.delete_user_application(request, obj_id)


class MyApplicationsTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_('Id'))
    instance = tables.Column('instance_name',
                             link=get_instance_link,
                             verbose_name=_('Instance'))
    app = tables.Column('application_name', verbose_name=_('Application'))
    version = tables.Column('version', verbose_name=_('Version'))
    uptime = tables.Column('uptime', verbose_name=_('Uptime'))
    
    def get_object_id(self, app):
        return app.id

    class Meta:
        name = "my_applications"
        verbose_name = _("Installed Applications")
        table_actions = (DeleteInstance,)
        row_actions = (DeleteInstance,)
