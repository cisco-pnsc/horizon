from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.admin import dashboard

__author__ = "Sergey Sudakovich", "Abishek Subramanian"
__email__ = "ssudakov@cisco.com", "absubram@cisco.com"


class Nexus1000v(horizon.Panel):
    name = _("Cisco Nexus 1000v")
    slug = 'nexus1000v'
    permissions = ('openstack.services.network',)

dashboard.Admin.register(Nexus1000v)
