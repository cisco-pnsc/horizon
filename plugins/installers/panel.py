from django.utils.translation import ugettext_lazy as _

import horizon

from plugins import dashboard


class Installers(horizon.Panel):
    name = _("Installers")
    slug = "installers"


dashboard.Plugins.register(Installers)
