# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 NEC Corporation
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.datastructures import SortedDict

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard import api


LOG = logging.getLogger(__name__)


class CreateNetwork(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           required=False)
    tenant_id = forms.ChoiceField(label=_("Project"))
    if (api.neutron.CISCO_N1K == True):
        n1kv_profile_id = forms.ChoiceField(label=_("Network Profile"))
    admin_state = forms.BooleanField(label=_("Admin State"),
                                     initial=True, required=False)
    shared = forms.BooleanField(label=_("Shared"),
                                initial=False, required=False)
    external = forms.BooleanField(label=_("External Network"),
                                  initial=False, required=False)

    @classmethod
    def _instantiate(cls, request, *args, **kwargs):
        return cls(request, *args, **kwargs)

    def __init__(self, request, *args, **kwargs):
        super(CreateNetwork, self).__init__(request, *args, **kwargs)
        tenant_choices = [('', _("Select a project"))]
        tenants, has_more = api.keystone.tenant_list(request)
        for tenant in tenants:
            if tenant.enabled:
                tenant_choices.append((tenant.id, tenant.name))
        self.fields['tenant_id'].choices = tenant_choices

        if (api.neutron.CISCO_N1K == True):
            self.fields['n1kv_profile_id'].choices = \
            self.get_network_profile_choices(request)

    def get_network_profile_choices(self,request):
        profile_choices = [('', _("Select a profile"))]
        for profile in self._get_profiles(request, 'network'):
            profile_choices.append((profile.id, profile.name))
        return profile_choices

    def _get_profiles(self, request, type_p):
        try:
            profiles = api.neutron.profile_list(request, type_p)
        except:
            profiles = []
            msg = _('Network Profiles could not be retrieved.')
            exceptions.handle(request, msg)
        if profiles:
            tenant_dict = self._get_tenant_list(request)
            #for p in profiles:
                #LOG.error("AAAAA profile name %s " % p)
            # Set tenant name
                #tenant = tenant_dict.get(p.tenant_id, None)
                #p.tenant_name = getattr(tenant, 'name', None)
        return profiles

    def _get_tenant_list(self, request):
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
 
    def handle(self, request, data):
        try:
            params = {'name': data['name'],
                      'tenant_id': data['tenant_id'],
                      'admin_state_up': data['admin_state'],
                      'shared': data['shared'],
                      'router:external': data['external']}
            if (api.neutron.CISCO_N1K == True):
                params['n1kv_profile_id'] =  data['n1kv_profile_id']
            network = api.neutron.network_create(request, **params)
            msg = _('Network %s was successfully created.') % data['name']
            LOG.debug(msg)
            messages.success(request, msg)
            return network
        except:
            redirect = reverse('horizon:admin:networks:index')
            msg = _('Failed to create network %s') % data['name']
            exceptions.handle(request, msg, redirect=redirect)


class UpdateNetwork(forms.SelfHandlingForm):
    name = forms.CharField(label=_("Name"), required=False)
    tenant_id = forms.CharField(widget=forms.HiddenInput)
    network_id = forms.CharField(label=_("ID"),
                                 widget=forms.TextInput(
                                     attrs={'readonly': 'readonly'}))
    admin_state = forms.BooleanField(label=_("Admin State"), required=False)
    shared = forms.BooleanField(label=_("Shared"), required=False)
    external = forms.BooleanField(label=_("External Network"), required=False)
    failure_url = 'horizon:admin:networks:index'

    def handle(self, request, data):
        try:
            params = {'name': data['name'],
                      'admin_state_up': data['admin_state'],
                      'shared': data['shared'],
                      'router:external': data['external']}
            network = api.neutron.network_modify(request, data['network_id'],
                                                 **params)
            msg = _('Network %s was successfully updated.') % data['name']
            LOG.debug(msg)
            messages.success(request, msg)
            return network
        except:
            msg = _('Failed to update network %s') % data['name']
            LOG.info(msg)
            redirect = reverse(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)
