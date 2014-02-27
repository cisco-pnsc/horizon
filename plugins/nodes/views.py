from horizon import tabs
from horizon import tables
from horizon import forms
from horizon import exceptions

from .tables import NodesTable
from .tabs import NodeDetailTabs
from .models import Node

from horizon.utils import memoized

import plugins.api.razor as razor_api
import plugins.api.accessories as accessories

class IndexView(tables.DataTableView):
    tab_group_class  = NodeDetailTabs
    table_class = NodesTable
    template_name = 'plugins/nodes/index.html'
	
    def get_data(self):
	res = []
	for k,v in accessories.convert(razor_api.get_all_nodes()).items():
		res.append(Node(v["name"],v["id"],v["status"],v["ipaddress"]))
	return res

class DetailView(tabs.TabView):
    tab_group_class = NodeDetailTabs
    template_name = 'plugins/nodes/detail.html'
        
class LogView(tabs.TabView):
    tab_group_class = NodeDetailTabs

