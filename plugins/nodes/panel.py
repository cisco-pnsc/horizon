from django.utils.translation import ugettext_lazy as _

import horizon

from plugins import dashboard


class Nodes(horizon.Panel):
    name = _("Nodes")
    slug = "nodes"


dashboard.Plugins.register(Nodes)
