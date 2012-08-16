# vim: tabstop=4 shiftwidth=4 softtabstop=4

<<<<<<< HEAD
# Copyright 2012 Cisco Systems Inc.
=======
# Copyright 2012 NEC Corporation
>>>>>>> master
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
<<<<<<< HEAD

import logging

from cloudfiles.errors import ContainerNotEmpty
from django import shortcuts
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.defaultfilters import filesizeformat
from django.utils import http
from django.utils.translation import ugettext as _

from horizon import api
=======
import logging

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import api
from horizon import exceptions
>>>>>>> master
from horizon import tables


LOG = logging.getLogger(__name__)


<<<<<<< HEAD
class DeleteNetworks(tables.DeleteAction):
    data_type_singular = _("Network")
    data_type_plural = _("Networks")

    def delete(self, request, obj_id):
        api.quantum_network_delete(request, obj_id)
=======
class DeleteNetwork(tables.DeleteAction):
    data_type_singular = _("Network")
    data_type_plural = _("Networks")

    def delete(self, request, network_id):
        try:
            # Retrieve existing subnets belonging to the network.
            subnets = api.quantum.subnet_list(request, network_id=network_id)
            LOG.debug('Network %s has subnets: %s' %
                      (network_id, [s.id for s in subnets]))
            for s in subnets:
                api.quantum.subnet_delete(request, s.id)
                LOG.debug('Deleted subnet %s' % s.id)

            api.quantum.network_delete(request, network_id)
            LOG.debug('Deleted network %s successfully' % network_id)
        except:
            msg = _('Failed to delete network %s') % network_id
            LOG.info(msg)
            redirect = reverse("horizon:nova:networks:index")
            exceptions.handle(request, msg, redirect=redirect)
>>>>>>> master


class CreateNetwork(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Network")
    url = "horizon:nova:networks:create"
    classes = ("ajax-modal", "btn-create")


<<<<<<< HEAD
class NetworksTable(tables.DataTable):
    name = tables.Column("name", link='horizon:nova:networks:ports:ports',
                         verbose_name=_("Network Name"))
    id = tables.Column("id", link='horizon:nova:networks:ports:ports',
                       verbose_name=_("Network id"))
    port_count = tables.Column("port_count", verbose_name=_('Ports'),
                               empty_value="0")

    def get_object_id(self, network):
        return network.id
=======
class EditNetwork(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit Network")
    url = "horizon:nova:networks:update"
    classes = ("ajax-modal", "btn-edit")


class CreateSubnet(tables.LinkAction):
    name = "subnet"
    verbose_name = _("Add Subnet")
    url = "horizon:nova:networks:addsubnet"
    classes = ("ajax-modal", "btn-create")


def get_subnets(network):
    template_name = 'nova/networks/_network_ips.html'
    context = {"subnets": network.subnets}
    return template.loader.render_to_string(template_name, context)


class NetworksTable(tables.DataTable):
    name = tables.Column("name",
                         verbose_name=_("Name"),
                         link='horizon:nova:networks:detail')
    subnets = tables.Column(get_subnets,
                            verbose_name=_("Subnets Associated"),)
    status = tables.Column("status", verbose_name=_("Status"))
    admin_state = tables.Column("admin_state",
                                verbose_name=_("Admin State"))
>>>>>>> master

    class Meta:
        name = "networks"
        verbose_name = _("Networks")
<<<<<<< HEAD
        table_actions = (CreateNetwork, DeleteNetworks,)
        row_actions = (DeleteNetworks,)
=======
        table_actions = (CreateNetwork, DeleteNetwork)
        row_actions = (EditNetwork, CreateSubnet, DeleteNetwork)
>>>>>>> master
