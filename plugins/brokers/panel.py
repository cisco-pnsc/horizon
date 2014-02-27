from django.utils.translation import ugettext_lazy as _

import horizon

from plugins import dashboard


class Brokers(horizon.Panel):
    name = _("Brokers")
    slug = "brokers"


dashboard.Plugins.register(Brokers)
