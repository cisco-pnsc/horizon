import logging

from horizon import tables
from django.utils.translation import ugettext_lazy as _

import plugins.api.razor as razor_api

LOG = logging.getLogger(__name__)

class TerminateRepo(tables.BatchAction):
    name = "terminate"
    action_present = _("Terminate")
    action_past = _("Terminate Repo: ")
    data_type_singular = _("Repo")
    data_type_plural = _("Repos")
    classes = ('btn-danger', 'btn-terminate')

    def allowed(self, request, repo=None):
        return True

    def action(self, request, obj_id):
        razor_api.delete_repo(obj_id)
        msg = _('Terminated Repo "%s"') % obj_id
        LOG.info(msg)

class RepoFilterAction(tables.FilterAction):

    def filter(self, table, repos, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()
        return [repo for repo in repos
                if q in repo.name.lower()]

class CreateRepo(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Repository")
    url = "horizon:plugins:repos:create"
    classes = ("ajax-modal", "btn-create")

class ReposTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Name"))
    iso_url = tables.Column('iso_url', verbose_name=_("ISO Url"))
  
    class Meta:
        name = "repositories"
        verbose_name = _("Repositories")
        table_actions = (CreateRepo,TerminateRepo,RepoFilterAction,)
        row_actions = (TerminateRepo,)
