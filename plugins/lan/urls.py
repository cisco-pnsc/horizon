from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa
from django.conf.urls.defaults import include  # noqa


from plugins.lan import views as views

VIEW_MOD = 'plugins.lan.views'

from plugins.lan.vlans import urls as vlans_url
from plugins.lan.modify_vlans import urls as modify_vlans_url
   
urlpatterns = patterns(VIEW_MOD,
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'vlans/', include(vlans_url, namespace='vlans')),
    url(r'modify_vlans/', include(modify_vlans_url, namespace='modify_vlans')),
)
