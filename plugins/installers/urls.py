from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from plugins.installers import views as views

VIEW_MOD = 'horizon.plugins.installers.views'

urlpatterns = patterns('VIEW_MOD',
    url(r'^$', views.CreateView.as_view(), name='index'),
)
