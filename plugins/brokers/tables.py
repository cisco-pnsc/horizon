import logging

from django.utils.translation import ugettext_lazy as _

from horizon import tables

LOG = logging.getLogger(__name__)

class BrokerFilterAction(tables.FilterAction):

    def filter(self, table, brokers, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()
        return [broker for broker in brokers
                if q in broker.name.lower()]

class CreateBroker(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Broker")
    url = "horizon:plugins:brokers:create"
    classes = ("ajax-modal", "btn-create")

class BrokersTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Name"))
    configuration_server = tables.Column('configuration_server', verbose_name=_("Configuration Server"))
    configuration_version = tables.Column('configuration_version', verbose_name=_("Configuration Version"))
    broker_type = tables.Column('broker_type', verbose_name=_("Broker Type"))
  
    class Meta:
        name = "brokers"
        verbose_name = _("Brokers")
        table_actions = (CreateBroker,BrokerFilterAction,)
        multi_select = False
