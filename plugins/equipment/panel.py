from django.utils.translation import ugettext_lazy as _

import horizon

from plugins import dashboard


class Equipment(horizon.Panel):
    name = _("Equipment")
    slug = "equipment"


dashboard.Plugins.register(Equipment)
