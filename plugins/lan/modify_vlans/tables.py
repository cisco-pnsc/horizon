from django.utils.translation import ugettext_lazy as _

from horizon import tables

class ProfilesAndTemplatesFilterAction(tables.FilterAction):

    def filter(self, table, profiles, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()
        return [profile for profile in profiles
                if q in profile.name.lower()]
        
class ModifyVlan(tables.LinkAction):
    name = "modify_vlan"
    verbose_name = _("Modify Vlan")
    url = "horizon:plugins:lan:modify_vlans:modify"
    classes = ("btn-edit")     

class TemplatesTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Name"))
    kind = tables.Column('type', verbose_name=_("Type"))
    
    class Meta:
        name = "templates"
        verbose_name = _("Templates")
        table_actions = (ProfilesAndTemplatesFilterAction,)
        row_actions = (ModifyVlan,)
        multi_select = False

class AddVlan(tables.LinkAction):
    name = "Add_vlan"
    verbose_name = _("Add Vlan")
    url = "horizon:plugins:lan:modify_vlans:add"
    classes = ("ajax-modal","btn-add")         
        
class NicsTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Name"))
    
    class Meta:
        name = "nics"
        verbose_name = _("Nics")
        row_actions = (AddVlan,)
        multi_select = False
        



