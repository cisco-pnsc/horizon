from django.utils.translation import ugettext_lazy as _

import horizon
from horizon.dashboards.syspanel import dashboard


class Hosts(horizon.Panel):
    name = _("Hosts")
    slug = 'hosts'
    roles = ('admin',)


dashboard.Syspanel.register(Hosts)
