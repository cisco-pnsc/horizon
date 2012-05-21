from django.utils.translation import ugettext_lazy as _

import horizon

from marketplace import dashboard


class My_Apps(horizon.Panel):
    name = _("Installed Applications")
    slug = "my_apps"


dashboard.Marketplace.register(My_Apps)
