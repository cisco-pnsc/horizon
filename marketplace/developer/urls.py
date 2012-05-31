from django.conf.urls.defaults import patterns, url

from .views import IndexView, CreateView, CreateVersionView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create/$', CreateView.as_view(), name='create'),
    url(r'^(?P<app_id>[^/]+)/create_version/$', CreateVersionView.as_view(), name='create_version'),
)
