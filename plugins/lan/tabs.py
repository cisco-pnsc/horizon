from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import exceptions
from horizon import tabs

from vlans.models import VLAN
from vlans.tables import VlansTable

from modify_vlans.models import Profile
from modify_vlans.tables import TemplatesTable

import plugins.api.accessories as accessories
import plugins.api.ucs as controller

class VlanTab(tabs.TableTab):
    table_classes = (VlansTable,)
    name = _("Vlans")
    slug = "vlans_tab"
    template_name = "horizon/common/_detail_table.html"

    def get_vlans_data(self):
        
        try:
            res = []
            for k, v in accessories.convert(controller.get_all_vlans()).items():
                res.append(VLAN(v['id'],v['name'], v['native'], v['nw_type'], v['locale'], v['owner'], v['multicast_policy_name'], 
                                v['multicast_policy_instance'], v['sharing_type'], v['fabric_id'], v['if_type'], v['transport_type']))
            return res
        except Exception:
            res = []
            exceptions.handle(self.request,
                              _('Unable to retrieve vlans.'))
        return res


class ModifyVlansTab(tabs.TableTab):
    table_classes = (TemplatesTable,)
    name = _("Modify Vlans")
    slug = "modify_vlans_tab"
    template_name = "horizon/common/_detail_table.html"

    def get_templates_data(self):
        
        try:
            res = []
            for k, v in accessories.convert(controller.get_all_templates()).items():
                res.append(Profile(v['id'], v['name'], v['type']))
            return res
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve templates.'))
        return res
    
class LanTabs(tabs.TabGroup):
    slug = "lan_tabs"
    tabs = (VlanTab,ModifyVlansTab)
    sticky = True
