<<<<<<< HEAD
from django.conf.urls.defaults import patterns, url

from .views import PortsView, CreatePortsView, AttachPortView, DetachPortView

PORTS = r'^(?P<port_id>[^/]+)/%s$'

# Quantum Network Ports
urlpatterns = patterns('horizon.dashboards.nova.networks.ports.views',
    url(
        r'^(?P<network_id>[^/]+)/ports/$',
        PortsView.as_view(),
        name='ports'),
    url(
        r'^(?P<network_id>[^/]+)/create/$',
        CreatePortsView.as_view(),
        name='create_ports'),
    url(
        r'^(?P<network_id>[^/]+)/(?P<port_id>[^/]+)/attach/$',
        AttachPortView.as_view(),
        name='attach_port'),
    url(
        r'^(?P<network_id>[^/]+)/(?P<port_id>[^/]+)/detach/$',
        DetachPortView.as_view(),
        name='detach_port'),
)
=======
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

from django.conf.urls.defaults import patterns, url

from .views import DetailView

PORTS = r'^(?P<port_id>[^/]+)/%s$'

urlpatterns = patterns('horizon.dashboards.nova.networks.ports.views',
    url(PORTS % 'detail', DetailView.as_view(), name='detail'))
>>>>>>> master
