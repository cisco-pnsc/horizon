from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from plugins.policies import views as views

VIEW_MOD = 'horizon.plugins.policies.views'

urlpatterns = patterns('VIEW_MOD',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create/$', views.CreateView.as_view(), name='create'),
)
