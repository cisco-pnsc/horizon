from django.utils.translation import ugettext_lazy as _

import horizon


#class PlatPanels(horizon.PanelGroup):
#    slug = "cisco"
#    name = _("Nexus Platform")
#    panels = ('nexus1000v')


class Cisco(horizon.Dashboard):
    name = _("Cisco")
    slug = "cisco"
    panels = ('nexus1000v',)  # Add your panels here.
    default_panel = 'nexus1000v'  # Specify the slug of the dashboard's default panel.
    permissions = ('openstack.roles.admin',)


horizon.register(Cisco)
