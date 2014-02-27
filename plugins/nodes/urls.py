from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from plugins.nodes import views as views

VIEW_MOD = 'horizon.plugins.nodes.views'

urlpatterns = patterns(VIEW_MOD,
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<node_id>[^/]+)$',
        views.DetailView.as_view(), name='detail'),
    url(r'^(?P<node_id>[^/]+)$',
        views.LogView.as_view(), name='log'),
)
