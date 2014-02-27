from django.utils.translation import ugettext_lazy as _

import horizon

from plugins import dashboard


class Lan(horizon.Panel):
    name = _("Lan")
    slug = "lan"


dashboard.Plugins.register(Lan)
