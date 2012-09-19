from django.conf.urls.defaults import *
from django.conf import settings

from .views import HostsView, HostDetailView

urlpatterns = patterns('horizon.dashboards.syspanel.hosts.views',
    url(r'^$', HostsView.as_view(), name='index'),
    url(r'^(?P<host_id>[^/]+)/details', HostDetailView.as_view(), name='details'),
)
