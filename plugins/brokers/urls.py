from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from plugins.brokers import views as views

VIEW_MOD = 'horizon.plugins.brokers.views'

urlpatterns = patterns('VIEW_MOD',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create/$', views.CreateView.as_view(), name='create'),
)
