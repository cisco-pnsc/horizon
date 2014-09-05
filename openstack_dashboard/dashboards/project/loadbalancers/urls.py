# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Copyright 2013, Big Switch Networks, Inc.
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

from django.conf.urls.defaults import patterns  # noqa
from django.conf.urls.defaults import url  # noqa

from openstack_dashboard.dashboards.project.loadbalancers import views


urlpatterns = patterns(
    'openstack_dashboard.dashboards.project.loadbalancers.views',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^addpool$', views.AddPoolView.as_view(), name='addpool'),
    url(r'^updatepool/(?P<pool_id>[^/]+)/$',
        views.UpdatePoolView.as_view(), name='updatepool'),
    url(r'^addvip/(?P<pool_id>[^/]+)/$',
        views.AddVipView.as_view(), name='addvip'),
    url(r'^updatevip/(?P<vip_id>[^/]+)/$',
        views.UpdateVipView.as_view(), name='updatevip'),
    url(r'^addmember$', views.AddMemberView.as_view(), name='addmember'),
    url(r'^updatemember/(?P<member_id>[^/]+)/$',
        views.UpdateMemberView.as_view(), name='updatemember'),
    url(r'^addmonitor$', views.AddMonitorView.as_view(), name='addmonitor'),
    url(r'^updatemonitor/(?P<monitor_id>[^/]+)/$',
        views.UpdateMonitorView.as_view(), name='updatemonitor'),
    url(r'^association/add/(?P<pool_id>[^/]+)/$',
        views.AddPMAssociationView.as_view(), name='addassociation'),
    url(r'^association/delete/(?P<pool_id>[^/]+)/$',
        views.DeletePMAssociationView.as_view(), name='deleteassociation'),
    url(r'^pool/(?P<pool_id>[^/]+)/$',
        views.PoolDetailsView.as_view(), name='pooldetails'),
    url(r'^vip/(?P<vip_id>[^/]+)/$',
        views.VipDetailsView.as_view(), name='vipdetails'),
    url(r'^member/(?P<member_id>[^/]+)/$',
        views.MemberDetailsView.as_view(), name='memberdetails'),
    url(r'^monitor/(?P<monitor_id>[^/]+)/$',
        views.MonitorDetailsView.as_view(), name='monitordetails'),
    url(r'^addsslpolicy$', views.AddSSLpolicyView.as_view(), name='addsslpolicy'),
    url(r'^addcertificate$', views.AddSSLcertificateView.as_view(), name='addcertificate'),
    url(r'^sslpolicy/(?P<sslpolicy_id>[^/]+)/$',
        views.SSLpolicyDetailsView.as_view(), name='sslpolicydetails'),
    url(r'^updatesslpolicy/(?P<sslpolicy_id>[^/]+)/$',
        views.UpdateSSLpolicyView.as_view(), name='updatesslpolicy'),
    url(r'^sslcertificatedetails/(?P<sslcertificate_id>[^/]+)/$',
        views.SSLcertificateDetailsView.as_view(), name='sslcertificatedetails'),
    url(r'^updatesslcertificate/(?P<sslcertificate_id>[^/]+)/$',
        views.UpdateSSLcertificateView.as_view(), name='updatesslcertificate'),
    url(r'^associatesslpolicy/(?P<vip_id>[^/]+)/$',
        views.AssociateSSLPolicyView.as_view(), name='associatesslpolicy'),
    url(r'^disassociatesslpolicy/(?P<vip_id>[^/]+)/$',
        views.DisassociateSSLPolicyView.as_view(), name='disassociatesslpolicy'))
