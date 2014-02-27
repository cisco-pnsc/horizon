from horizon import tabs

from .tabs import LanTabs

class IndexView(tabs.TabbedTableView):
    tab_group_class = LanTabs
    template_name = 'plugins/lan/index.html'
    