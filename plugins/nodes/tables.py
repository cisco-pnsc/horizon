import logging

from horizon import tables
from horizon import messages

from django.utils.translation import ugettext_lazy as _

import plugins.api.razor as razor_api

from .models import Node

LOG = logging.getLogger(__name__)

class TerminateInstance(tables.BatchAction):
    name = "terminate"
    action_present = _("Terminate")
    action_past = _("Scheduled termination of")
    data_type_singular = _("Node")
    data_type_plural = _("Nodes")
    classes = ('btn-danger', 'btn-terminate')

    def allowed(self, request, node=None):
        return True

    def action(self, request, obj_id):
        razor_api.delete_node(obj_id)
        msg = _('Terminated Node "%s"') % obj_id
        LOG.info(msg)

class NodeFilterAction(tables.FilterAction):

    def filter(self, table, instances, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()
        return [instance for instance in instances
                if q in instance.name.lower()]

class UnbindNode(tables.BatchAction):
    name = "unbind_node"
    data_type_singular = _("Node")
    classes = ('btn-danger', 'btn-unbind')
    action_present = _("Unbind")
    action_past = _("Unbound")

    def action(self, request, obj_id):
        razor_api.unbind_node(obj_id)
        msg = _('Unbind Node "%s"') % obj_id
        LOG.info(msg)


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, node_id):
        node = razor_api.get_node_details(node_id)

        if 'details' in node.keys():
            messages.error(request, node['details'])
            return Node(node['name'],'','')
        return Node(node['name'],node['spec'],node['status'],node['ipaddress'],node['log_link'],node['policy'],node['tags'])

DISPLAY_CHOICES = (
    ("Boot", _("Booting")),
    ("Bind", _("Bind")),
    ("Installer", _("Installer")),
    ("Unbound", _("Unbound")),
    ("Broker", _("Done")),
)

class NodesTable(tables.DataTable):

    STATUS_CHOICES = (
        ('Unbound', True),
        ('Done', True),
    )

    name = tables.Column('name', verbose_name=_("Name"),link='horizon:plugins:nodes:detail')
    ipaddress = tables.Column('ipaddress', verbose_name=_("IP Address"))
    spec = tables.Column('spec', verbose_name=_("Spec"))
    status = tables.Column('status', verbose_name=_("Status"),status=True,
			    display_choices=DISPLAY_CHOICES,
			    status_choices=STATUS_CHOICES)

    class Meta:
        name = "nodes"
        verbose_name = _("Nodes")
        status_columns = ["status"]
        row_class = UpdateRow
        table_actions = (TerminateInstance,NodeFilterAction,)
        row_actions = (TerminateInstance,UnbindNode)
