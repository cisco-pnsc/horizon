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

from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from openstack_dashboard.dashboards.cisco.nexus1000v.views \
    import CreateNetworkProfileView
from openstack_dashboard.dashboards.cisco.nexus1000v.views import IndexView
from openstack_dashboard.dashboards.cisco.nexus1000v.views \
    import UpdateNetworkProfileView

NETWORKS_PROFLIE = r'^network_profile/(?P<network_id>[^/]+)/%s$'

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    #Network Profile
# url(r'^network_profile$', NetworkProfileIndexView.as_view(),
# name='network_profile'),
    url(r'^network_profile/create$', CreateNetworkProfileView.as_view(),
        name='create_network_profile'),
    url(r'^network_profile/(?P<profile_id>[^/]+)/update$',
        UpdateNetworkProfileView.as_view(), name='update_network_profile'),
    #Policy Profile
# url(r'^policy_profile$', PolicyProfileIndexView.as_view(),
# name='policy_profile'),

)
