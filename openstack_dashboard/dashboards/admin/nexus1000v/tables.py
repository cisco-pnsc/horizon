import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables

from openstack_dashboard import api

from .forms import CreateNetworkProfile

# from openstack_dashboard import api

__author__ = "Sergey Sudakovich"
__email__ = "ssudakov@cisco.com"

LOG = logging.getLogger(__name__)

class CreateNetworkProfile(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Network Profile")
    url = "horizon:admin:nexus1000v:create_network_profile"
    classes = ("ajax-modal", "btn-create")

class DeleteNetworkProfile(tables.DeleteAction):
    data_type_singular = _("Network Profile")
    data_type_plural = _("Netork Profiles")

    def delete(self, request, obj_id):
        try:
            LOG.error("AAAAAAprofile_delete(): profile_id= %s " % 
                      obj_id, )
            api.quantum.profile_delete(request, obj_id)
        except:
            msg = _('Failed to delete network profile %s') % obj_id
            LOG.info(msg)
            redirect = reverse('horizon:admin:nexus1000v:index')
            exceptions.handle(request, msg, redirect=redirect)


class EditNetworkProfile(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit Network Profile")
    url = "horizon:admin:nexus1000v:update_networkprofile"
    classes = ("ajax-modal", "btn-edit")


class NetworkProfile(tables.DataTable):
    id = tables.Column("profile_id", verbose_name=_("Profile ID"), hidden=True)
    name = tables.Column("name", verbose_name=_("Network Profile"), )
    tenant = tables.Column("tenant_name", verbose_name=_("Tenant"))
    segment_type = tables.Column("segment_type", verbose_name=_("Segment Type"))
    segment_range = tables.Column("segment_range", verbose_name=_("Segment Range"))

    class Meta:
        name = "network_profile"
        verbose_name = _("Network Profile")
        table_actions = (CreateNetworkProfile, DeleteNetworkProfile,)
        row_actions = (EditNetworkProfile,DeleteNetworkProfile,)


class EditPolicyProfile(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit Policy Profile")
    url = "horizon:project:images_and_snapshots:images:update"
    classes = ("ajax-modal", "btn-edit")


class PolicyProfile(tables.DataTable):
    id = tables.Column("profile_id", verbose_name=_("Profile ID"), hidden=True)
    name = tables.Column("name", verbose_name=_("Policy Profile"), )
    tenant_id = tables.Column("tenant_id", verbose_name=_("Tenant"))
    segment_type = tables.Column("segment_type", verbose_name=_("Segment Type"))
    segment_range = tables.Column("segment_range", verbose_name=_("Segment Range"))

    class Meta:
        name = "policy_profile"
        verbose_name = _("Policy Profile")
#        row_actions = (EditPolicyProfile,)
