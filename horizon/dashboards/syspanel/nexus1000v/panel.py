from django.utils.translation import ugettext_lazy as _

import horizon
from horizon.dashboards.syspanel import dashboard

__author__ = "Sergey Sudakovich"
__email__ = "ssudakov@cisco.com"


class Nexus1000v(horizon.Panel):
    name = _("Cisco Nexus 1000v")
    slug = 'nexus1000v'
    permissions = ('openstack.services.network',)

dashboard.Syspanel.register(Nexus1000v)
