from django.utils.translation import ugettext_lazy as _

import horizon

from plugins import dashboard


class Policies(horizon.Panel):
    name = _("Policies")
    slug = "policies"


dashboard.Plugins.register(Policies)
