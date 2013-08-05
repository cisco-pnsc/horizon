# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Cisco Systems, Inc.
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
#
# @author: Abishek Subramanian, Cisco Systems, Inc.
# @author: Sergey Sudakovich,   Cisco Systems, Inc.

import logging

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard import api

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


LOG = logging.getLogger(__name__)


def get_tenant_choices(request):
    tenant_choices = [('', _("Select a tenant"))]
    for tenant in api.keystone.tenant_list(request, admin=True):
        if tenant.enabled:
            tenant_choices.append((tenant.id, tenant.name))
    return tenant_choices


class CreateNetworkProfile(forms.SelfHandlingForm):
    """ Create Network Profile form """
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           required=True)
    segment_type = forms.ChoiceField(label=_('Segment Type'),
                                     choices=[('vlan', _('VLAN')),
                                              ('vxlan', _('VXLAN'))],
                                     widget=forms.Select
                                     (attrs={'class': 'switchable',
                                             'data-slug': 'segtype'}))
    segment_range = forms.CharField(max_length=11,
                                    label=_("Segment Range"),
                                    required=True,
                                    help_text=_("1-4093 for VLAN"))
    multicast_ip_range = forms.CharField(max_length=30,
                                         label=_("Multicast IP Range"),
                                         required=False,
                                         widget=forms.TextInput
                                         (attrs={'class': 'switched',
                                                 'data-switch-on':
                                                     'segtype',
                                                 'data-segtype-vxlan':
                                                     _("Multicast IP Range")}))
    physical_network = forms.CharField(max_length=255,
                                       label=_("Physical Network"),
                                       required=False,
                                       widget=forms.TextInput
                                       (attrs={'class': 'switched',
                                               'data-switch-on': 'segtype',
                                               'data-segtype-vlan':
                                                   _("Physical Network")}))
    tenant_id = forms.ChoiceField(label=_("Tenant"),
                                  required=False)

    def __init__(self, request, *args, **kwargs):
        super(CreateNetworkProfile, self).__init__(request, *args, **kwargs)
        self.fields['tenant_id'].choices = get_tenant_choices(request)

    def handle(self, request, data):
        try:
            profile = api.neutron.profile_create(request,
                                                 name=data['name'],
                                                 #profile_type='network',
                                                 segment_type=
                                                 data['segment_type'],
                                                 segment_range=
                                                 data['segment_range'],
                                                 physical_network=
                                                 data['physical_network'],
                                                 multicast_ip_range=
                                                 data['multicast_ip_range'],
                                                 tenant_id=data['tenant_id'])
            msg = _('Network Profile %s was successfully created.')\
                % data['name']
            LOG.debug(msg)
            messages.success(request, msg)
            return profile
        except:
            redirect = reverse('horizon:cisco:nexus1000v:index')
            msg = _('Failed to create network profile %s') % data['name']
            exceptions.handle(request, msg, redirect=redirect)


class UpdateNetworkProfile(forms.SelfHandlingForm):
    """ Update Network Profile form """
    profile_id = forms.CharField(label=_("ID"),
                                 widget=forms.HiddenInput())
    name = forms.CharField(max_length=255,
                           label=_("Name"), required=True)
    segment_type = forms.ChoiceField(label=_('Segment Type'),
                                     choices=[('vlan', 'VLAN'),
                                              ('vxlan', 'VXLAN')],
                                     widget=forms.Select
                                     (attrs={'class': 'switchable'}))

    segment_range = forms.CharField(max_length=10,
                                    label=_("Segment Range"),
                                    required=True)
    physical_network = forms.CharField(max_length=255,
                                       label=_("Physical Network"),
                                       required=False)
    tenant_id = forms.CharField(label=_("Tenant"), required=False)

    def handle(self, request, data):
        try:
            LOG.debug('request = %s' % request)
            LOG.debug('params = %s' % data)
            profile = api.neutron.profile_modify(request,
                                                 data['profile_id'],
                                                 name=data['name'],
                                                 segment_type=
                                                 data['segment_type'],
                                                 segment_range=
                                                 data['segment_range'],
                                                 physical_network=
                                                 data['physical_network'])
            msg = _('Network Profile %s was successfully updated.')\
                  % data['profile_id']
            LOG.debug(msg)
            messages.success(request, msg)
            return profile
        except Exception:
            msg = _('Failed to update network profile %s') % data['profile_id']
            LOG.info(msg)
            redirect = reverse('horizon:cisco:nexus1000v:index')
            exceptions.handle(request, msg, redirect=redirect)
