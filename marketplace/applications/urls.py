from django.conf.urls.defaults import patterns, url

from .views import IndexView, DetailView, StartView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<app_id>[^/]+)/$', DetailView.as_view(), name='details'),
    url(r'^(?P<app_id>[^/]+)/start$', StartView.as_view(), name='start'),
)
