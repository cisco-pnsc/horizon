from django.utils.translation import ugettext_lazy as _

import horizon

from plugins import dashboard


class Repos(horizon.Panel):
    name = _("Repositories")
    slug = "repos"


dashboard.Plugins.register(Repos)
