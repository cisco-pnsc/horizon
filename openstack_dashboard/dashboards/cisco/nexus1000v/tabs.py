__author__ = 'ssudakov'

from django.utils.translation import ugettext as _

from horizon import tabs

class NetworkProfileTab(tabs.Tab):
    name = _("Network Profile")
    slug = "network_profile"
    template_name = 'cisco/nexus1000v/network_profile/index.html'

    def get_context_data(self, request):
        return None


class PolicyProfileTab(tabs.Tab):
    name = _("Policy Profile")
    slug = "policy_profile"
    template_name = 'cisco/nexus1000v/policy_profile/index.html'
    preload = False

class IndexTabs(tabs.TabGroup):
    slug = "indextabs"
    tabs = (NetworkProfileTab, PolicyProfileTab)
