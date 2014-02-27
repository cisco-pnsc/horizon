from django.utils.translation import ugettext_lazy as _

import horizon

class UCSApi(horizon.PanelGroup):
    slug = "ucs_api"
    name = _("UCS API")
    panels = ('equipment','lan',)

class RazorApi(horizon.PanelGroup):
    slug = "razor_api"
    name = _("Razor API")
    panels = ('nodes','repos','brokers','installers','tags','policies')

class Plugins(horizon.Dashboard):
    name = _("Plugins")
    slug = "plugins"
    panels = (RazorApi,UCSApi,)
    default_panel = 'nodes'
  
horizon.register(Plugins)
