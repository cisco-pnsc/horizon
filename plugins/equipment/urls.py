from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from plugins.equipment import views as views

VIEW_MOD = 'plugins.equipment.views'


urlpatterns = patterns(VIEW_MOD,
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<server_id>[^/]+)$',views.DetailView.as_view(), name='detail'),
    url(r'^(?P<server_id>[^/]+)/associate$', views.AssociateServiceProfileView.as_view(), name='associate'),
    url(r'^(?P<server_id>[^/]+)/dissociate$', views.DisassociateServiceProfileView.as_view(), name='dissociate'),
    url(r'^(?P<server_id>[^/]+)/shutdown$', views.ShutdownServerView.as_view(), name='shutdown'),
    url(r'^multiple_assign/$', views.AssociateMultipleServiceProfilesView.as_view(), name='associate_multiple'),
    url(r'^(?P<server_id>[^/]+)/console$', 'console', name='console'),
    url(r'^download/$', views.DownloadDataView.as_view(), name='download'),
    url(r'^download_data/$', views.download_data, name='download_data'),
    
    
)
