# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Cisco Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
import copy

from cloudfiles.errors import ContainerNotEmpty
from django import shortcuts
from django.contrib import messages
from django.core import urlresolvers
from django.template.defaultfilters import filesizeformat
from django.utils import http
from django.utils.translation import ugettext as _

from horizon import api
from horizon import tables

from horizon.tables.actions import FilterAction, LinkAction

import re


LOG = logging.getLogger(__name__)


class CreatePorts(tables.LinkAction):
    name = "create_ports"
    verbose_name = _("Create Ports")
    classes = ("ajax-modal", "btn-create")

    def get_link_url(self, datum=None):
        network_id = self.table.kwargs['network_id']
        return urlresolvers.reverse(
            'horizon:nova:networks:ports:create_ports', 
            args=[network_id])


class DeletePorts(tables.DeleteAction):
    data_type_singular = _("Port")
    data_type_plural = _("Ports")

    def get_network_id(self, request):
        uri = request.META['REQUEST_URI']
        match = re.search('/nova/networks/([^/]+)/ports', uri)
        network_id = match.group(1)

        return network_id

    def delete(self, request, obj_id):
        network_id = self.get_network_id(request)
        api.quantum_port_delete(request, network_id, obj_id)

    def handle(self, table, request, object_ids):
        # Overriden to show clearer error messages instead of generic message
        deleted = []
        for obj_id in object_ids:
            obj = table.get_object_by_id(obj_id)
            try:
                self.delete(request, obj_id)
                deleted.append(obj)
            except:
                LOG.exception('Unable to delete port "%s".' % obj.id)
                messages.error(request,
                               _('Unable to delete port: %s') %
                               obj.id)
                raise
        if deleted:
            messages.success(request,
                             _('Successfully deleted port: %s')
                               % ", ".join([obj.id for obj in deleted]))
        network_id = self.get_network_id(request)
        return shortcuts.redirect(
            'horizon:nova:networks:ports:ports', 
            network_id=network_id)


class AttachPort(tables.LinkAction):
    name = "attach_port"
    verbose_name = _("Attach Port")
    classes = ("ajax-modal", "btn-success")

    def get_link_url(self, datum=None):
        network_id = self.table.kwargs['network_id']
        return urlresolvers.reverse(
            'horizon:nova:networks:ports:attach_port',
            args=[network_id, datum.id])

class DetachPort(tables.LinkAction):
    name = "detach_port"
    verbose_name = _("Detach Port")
    classes = ("ajax-modal", "btn-danger", "btn-delete")
    
    def get_link_url(self, datum=None):
        network_id = self.table.kwargs['network_id']
        return urlresolvers.reverse(
            'horizon:nova:networks:ports:detach_port',
            args=[network_id, datum.id])

class PortsTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("Port id"))
    state = tables.Column("state", verbose_name=_("State"))
    op_status = tables.Column("op-status", verbose_name=_("Operational status"))
    attachment_server = tables.Column("attachment_server", verbose_name=_("Attachment"))

    def get_object_id(self, port):
        return port.id
    
    def get_row_actions(self, datum):
        self._meta.row_actions = []
        if datum.attachment_id:
            self._meta.row_actions.append(DetachPort)
        else:
            self._meta.row_actions.append(AttachPort)
        return super(PortsTable, self).get_row_actions(datum)

    class Meta:
        name = "ports"
        verbose_name = _("Ports")
        row_actions = (AttachPort,DetachPort,)
        table_actions = (CreatePorts, DeletePorts,)
