from django.conf.urls.defaults import *
from django.conf import settings

from .views import HostsView, HostDetailView, NetStatsView, CpuStatsView, MemStatsView, PartStatsView, DiskStatsView

urlpatterns = patterns('horizon.dashboards.syspanel.hosts.views',
    url(r'^$', HostsView.as_view(), name='index'),
    url(r'^(?P<host_id>[^/]+)/details', HostDetailView.as_view(), name='details'),

    url(r'^(?P<host_id>[^/]+)/net/(?P<int_id>[^/]+)/stats$',
        NetStatsView.as_view(), name='net_stats'),

    url(r'^(?P<host_id>[^/]+)/cpu/(?P<cpu_id>[^/]+)/stats$',
        CpuStatsView.as_view(), name='cpu_stats'),

    url(r'^(?P<host_id>[^/]+)/mem/(?P<mem_id>[^/]+)/stats$',
        MemStatsView.as_view(), name='mem_stats'),

    url(r'^(?P<host_id>[^/]+)/part/(?P<part_id>[^/]+)/stats$',
        PartStatsView.as_view(), name='part_stats'),

    url(r'^(?P<host_id>[^/]+)/disk/(?P<disk_id>[^/]+)/stats$',
        DiskStatsView.as_view(), name='disk_stats'),
)
