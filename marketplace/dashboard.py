from django.utils.translation import ugettext_lazy as _

import horizon

class Marketplace(horizon.Dashboard):
    name = _("Marketplace")
    slug = "marketplace"
    panels = ('applications',)
    default_panel = 'applications'
    supports_tenants = True


horizon.register(Marketplace)
