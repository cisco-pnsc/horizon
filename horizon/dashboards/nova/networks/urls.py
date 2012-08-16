# vim: tabstop=4 shiftwidth=4 softtabstop=4

<<<<<<< HEAD
# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Cisco Systems, Inc.
=======
# Copyright 2012 NEC Corporation
>>>>>>> master
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

<<<<<<< HEAD
from django.conf.urls.defaults import *

from .ports import urls as port_urls
from .views import IndexView, CreateNetworkView

NETWORKS = r'^(?P<network_id>[^/]+)/%s$'

# Quantum Networks and Ports
urlpatterns = patterns('horizon.dashboards.nova.networks.views',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create/$', CreateNetworkView.as_view(), name='create'),
    url(r'', include(port_urls, namespace='ports'))
)
=======
from django.conf.urls.defaults import patterns, url, include

from .views import IndexView, CreateView, DetailView, UpdateView
from .subnets.views import CreateView as AddSubnetView
from .subnets.views import UpdateView as EditSubnetView
from .subnets import urls as subnet_urls
from .ports import urls as port_urls

NETWORKS = r'^(?P<network_id>[^/]+)/%s$'

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create$', CreateView.as_view(), name='create'),
    url(NETWORKS % 'detail', DetailView.as_view(), name='detail'),
    url(NETWORKS % 'update', UpdateView.as_view(), name='update'),
    url(NETWORKS % 'subnets/create', AddSubnetView.as_view(),
        name='addsubnet'),
    url(r'^(?P<network_id>[^/]+)/subnets/(?P<subnet_id>[^/]+)/update$',
        EditSubnetView.as_view(), name='editsubnet'),
    url(r'^subnets/', include(subnet_urls, namespace='subnets')),
    url(r'^ports/', include(port_urls, namespace='ports')))
>>>>>>> master
