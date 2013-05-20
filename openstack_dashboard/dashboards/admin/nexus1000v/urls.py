from django.conf.urls.defaults import patterns, url
from .views import IndexView, CreateNetworkProfileView, UpdateNetworkProfileView

__author__ = "Sergey Sudakovich"
__email__ = "ssudakov@cisco.com"

NETWORKS_PROFLIE = r'^network_profile/(?P<network_id>[^/]+)/%s$'

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    #Network Profile
#    url(r'^network_profile$', NetworkProfileIndexView.as_view(),
#        name='network_profile'),
    url(r'^network_profile/create$', CreateNetworkProfileView.as_view(),
        name='create_network_profile'),
    url(r'^network_profile/(?P<profile_id>[^/]+)/update$',
        UpdateNetworkProfileView.as_view(), name='update_network_profile'),
    #Policy Profile
#    url(r'^policy_profile$', PolicyProfileIndexView.as_view(),
#        name='policy_profile'),

)
