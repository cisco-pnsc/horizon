from django.utils.translation import ugettext_lazy as _

import horizon

from marketplace import dashboard


class Developer(horizon.Panel):
    name = _("Developer")
    slug = "developer"


dashboard.Marketplace.register(Developer)
