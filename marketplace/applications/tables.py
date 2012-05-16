from django.utils.translation import ugettext_lazy as _
from horizon import tables

class ApplicationsTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_('Name'))
    desc = tables.Column('desc', verbose_name=_('Description'))

    class Meta:
        name = "applications"
        verbose_name = _("Applications")
