from django.utils.translation import ugettext_lazy as _
from horizon import tabs

import plugins.api.razor as razor_api


class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = "plugins/nodes/_detail_overview.html"

    def get_context_data(self, request):
        return {"node": razor_api.get_node_details(self.tab_group.kwargs['node_id'])}               

class LogTab(tabs.Tab):
    name = _("Log")
    slug = "log"
    template_name = "plugins/nodes/_detail_log.html"
    preload = False

    def get_context_data(self, request):
        node = self.tab_group.kwargs['node_id']
        try:
            data = razor_api.get_node_log(node)
        except Exception:
            data = _('Unable to get log for instance "%s".') % node
            exceptions.handle(request, ignore=True)
        return {"node": node,
                "log": data}

class NodeDetailTabs(tabs.TabGroup):
    slug = "node_details"
    tabs = (OverviewTab,LogTab,)
    sticky = True