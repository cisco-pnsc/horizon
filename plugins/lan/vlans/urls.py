from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from plugins.lan.vlans import views as views

VIEW_MOD = 'plugins.lan.vlans.views'


urlpatterns = patterns(VIEW_MOD,
    url(r'^create/$', views.CreateView.as_view(), name='create'),
    url(r'^create_mcpolicy/$', views.CreateMCPolicyView.as_view(), name='create_mcpolicy')
)
