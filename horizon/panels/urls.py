from django.conf.urls.defaults import *

from .views import PanelView

urlpatterns = patterns('horizon.panels.views',
    url(r'^$', PanelView.as_view(), name='index'),
)
