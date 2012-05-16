from django.utils.translation import ugettext_lazy as _

import horizon
from marketplace import dashboard


class Applications(horizon.Panel):
    name = _("Applications")
    slug = "applications"

dashboard.Marketplace.register(Applications)
