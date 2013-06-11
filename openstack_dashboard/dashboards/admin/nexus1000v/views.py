__author__ = "Sergey Sudakovich"
__email__ = "ssudakov@cisco.com"

import logging

from django.core.urlresolvers import reverse_lazy
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tables
from horizon import tabs
from horizon import views

from openstack_dashboard import api

from .forms import CreateNetworkProfile, UpdateNetworkProfile
from .tables import NetworkProfile, PolicyProfile
from .tabs import IndexTabs

LOG = logging.getLogger(__name__)


def _get_tenant_list(request):
    tenants = []
    try:
        tenants = api.keystone.tenant_list(request, admin=True)
    except:
        tenants = []
        msg = _('Unable to retrieve instance tenant information.')
        exceptions.handle(request, msg)

    tenant_dict = SortedDict([(t.id, t) for t in tenants])
    tenants = tenant_dict
    return tenants


def _get_profiles(request, type_p):
    try:
        profiles = api.quantum.profile_list(request, type_p)
    except:
        profiles = []
        msg = _('Network Profiles could not be retrieved.')
        exceptions.handle(request, msg)
    if profiles:
        tenant_dict = _get_tenant_list(request)
        bindings = api.quantum.profile_bindings_list(request, type_p)
        for p in profiles:
        # Set tenant name
            if bindings:
                for b in bindings:
                    if (p.id == b.profile_id):
                        tenant = tenant_dict.get(b.tenant_id, None)
                        p.tenant_name = getattr(tenant, 'name', None)
#            p.set_id_as_name_if_empty()
    return profiles

#class NetworkProfileIndexView(tabs.TableTab):
class NetworkProfileIndexView(tables.DataTableView):
    table_class = NetworkProfile
    template_name = 'admin/nexus1000v/network_profile/index.html'

    def get_data(self):
        return _get_profiles(self.request, 'network')



#class PolicyProfileIndexView(tabs.TableTab):
class PolicyProfileIndexView(tables.DataTableView):
    table_class = PolicyProfile
    template_name = 'admin/nexus1000v/policy_profile/index.html'

    def get_data(self):
        return _get_profiles(self.request, 'policy')

class IndexTabGroup(tabs.TabGroup):
    slug = "group"
    tabs = (NetworkProfileIndexView, PolicyProfileIndexView,)

#class IndexView(tabs.TabbedTableView):
#    tab_group_class = IndexTabs
#    template_name = 'syspanel/nexus1000v/index.html'
#
#    def get_network_profile_data(self):
#        return _get_profiles('network')
#
#    def get_policy_profile_data(self):
#        return _get_profiles('policy')

class IndexView(tables.MultiTableView):
    table_classes = (NetworkProfile, PolicyProfile,)
    template_name = 'admin/nexus1000v/index.html'

    def get_network_profile_data(self):
        return _get_profiles(self.request,'network')

    def get_policy_profile_data(self):
        return _get_profiles(self.request,'policy')


class CreateNetworkProfileView(forms.ModalFormView):
    form_class = CreateNetworkProfile
    template_name = 'admin/nexus1000v/create_network_profile.html'
    success_url = reverse_lazy('horizon:admin:nexus1000v:index')

class UpdateNetworkProfileView(forms.ModalFormView):
    form_class = UpdateNetworkProfile
    template_name = 'admin/nexus1000v/update_network_profile.html'
    context_object_name = 'network_profile'
    success_url = reverse_lazy('horizon:admin:nexus1000v:index')

    def get_context_data(self, **kwargs):
        context = super(UpdateNetworkProfileView, self).get_context_data(**kwargs)
        context["profile_id"] = self.kwargs['profile_id']
        return context

    def _get_object(self, *args, **kwargs):
        if not hasattr(self, "_object"):
            profile_id = self.kwargs['profile_id']
            try:
                self._object = api.quantum.profile_get(self.request, profile_id)
                LOG.debug("_object=%s" % self._object)
            except:
                redirect = self.success_url
                msg = _('Unable to retrieve network profile details.')
                exceptions.handle(self.request, msg, redirect=redirect)
        return self._object

    def get_initial(self):
        profile = self._get_object()
        return {'profile_id': profile['id'],
                'name': profile['name'],
                #'tenant_id': profile['tenant_id'],
                'segment_range': profile['segment_range'],
                'segment_type': profile['segment_type'],
                'physical_network': profile['physical_network']}
                #'profile_type': profile['profile_type']}

