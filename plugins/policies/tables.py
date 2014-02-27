import logging

from horizon import tables
from django.utils.translation import ugettext_lazy as _

import plugins.api.razor as razor_api

LOG = logging.getLogger(__name__)


class PolicyFilterAction(tables.FilterAction):

    def filter(self, table, policies, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()
        return [policy for policy in policies
                if q in policy.name.lower()]

class CreatePolicy(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Policy")
    url = "horizon:plugins:policies:create"
    classes = ("btn-create")

class EnablePolicy(tables.BatchAction):
    name = "enable_policy"
    data_type_singular = _("Policy")
    classes = ('btn-enable')
    action_present = _("Enable")
    action_past = _("Enabled")

    def allowed(self, request, policy=None):
        try:
            if policy is not None:
                return policy.enabled == False
            return False
        except:
            return False
        
    def action(self, request, obj_id):
        razor_api.enable_policy(obj_id)
        msg = _('Enabled Policy "%s"') % obj_id
        LOG.info(msg)

class DisablePolicy(tables.BatchAction):
    name = "disable_policy"
    data_type_singular = _("Policy")
    classes = ('btn-danger','btn-disable')
    action_present = _("Disable")
    action_past = _("Disabled")

    def allowed(self, request, policy=None):
        try:
            if policy is not None:
                return policy.enabled == True
            return False
        except:
            return False
        
    def action(self, request, obj_id):
        razor_api.disable_policy(obj_id)
        msg = _('Disabled Policy "%s"') % obj_id
        LOG.info(msg)



class PoliciesTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Policy Name"))
    repo = tables.Column('repo', verbose_name=_("Repo Name"))
    installer = tables.Column('installer', verbose_name=_("Installer Name"))
    broker = tables.Column('broker', verbose_name=_("Broker Name"))
    tags = tables.Column('tags', verbose_name=_("Tags"))
    hostname = tables.Column('hostname', verbose_name=_("Hostname"))
    password = tables.Column('root_password', verbose_name=_("Password"))
    max_count = tables.Column('max_count', verbose_name=_("Max Count"))
    rule_number = tables.Column('rule_number', verbose_name=_("Rule Number"))
    enabled = tables.Column('enabled', verbose_name=_("Enabled"))
    
  
    class Meta:
        name = "policies"
        verbose_name = _("Policies")
        table_actions = (CreatePolicy,PolicyFilterAction,)
        row_actions = (EnablePolicy, DisablePolicy,)
        multi_select = False
