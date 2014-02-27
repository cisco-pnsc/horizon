import logging

from horizon import tables

from django.utils.translation import ugettext_lazy as _

import plugins.api.ucs as ucs_api

LOG = logging.getLogger(__name__)

class VlanFilterAction(tables.FilterAction):

    def filter(self, table, vlans, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()
        return [vlan for vlan in vlans
                if q in vlan.name.lower()]

class CreateVlan(tables.LinkAction):
    name = "create_vlan"
    verbose_name = _("Create Vlan")
    url = "horizon:plugins:lan:vlans:create"
    classes = ("ajax-modal", "btn-create")


class DeleteVlan(tables.BatchAction):
    ajax = True
    name = "delete_vlan"
    data_type_singular = _("Vlan")
    data_type_plural = _("Vlans")
    classes = ('btn-danger', 'btn-terminate')
    action_present = _("Delete")
    action_past = _("Delete")
            
    def action(self, request, obj_id):
        ucs_api.delete_vlan(obj_id)


class VlansTable(tables.DataTable):
    
    name = tables.Column('name', verbose_name=_("Name"))
    native = tables.Column('native', verbose_name=_("Native"))
    nw_type = tables.Column('nw_type', verbose_name=_("Network Type"))
    locale = tables.Column('locale', verbose_name=_("Locale"))
    owner = tables.Column('owner', verbose_name=_("Owner"))
    multicast_policy_name = tables.Column('multicast_policy_name', verbose_name=_("Multicast Policy Name"))
    multicast_policy_instance = tables.Column('multicast_policy_instance', verbose_name=_("Multicast Policy Instance"))
    sharing_type = tables.Column('sharing_type', verbose_name=_("Sharing Type"))
    fabric_id = tables.Column('fabric_id', verbose_name=_("Fabric ID"))
    if_type = tables.Column('if_type', verbose_name=_("If Type"))
    transport_type = tables.Column('transport_type', verbose_name=_("Transport Type"))

    class Meta:
        name = "vlans"
        verbose_name = _("VLANS")
        table_actions = (VlanFilterAction,CreateVlan,DeleteVlan,)
        row_actions = (DeleteVlan,)
        multi_select = True
