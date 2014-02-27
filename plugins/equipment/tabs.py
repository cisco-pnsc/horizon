from django.utils.translation import ugettext_lazy as _

from horizon import tabs

import plugins.api.ucs as ucs_api


class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = "plugins/equipment/_detail_overview.html"

    def get_context_data(self, request):
        return {"server": ucs_api.get_server_details(self.tab_group.kwargs['server_id'])}               

class ServerDetailTabs(tabs.TabGroup):
    slug = "server_details"
    tabs = (OverviewTab,)