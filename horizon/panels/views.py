import sys
import time
import logging

from django.http import HttpResponse

from horizon import views
from horizon.api.monitoring import monitorclient
from horizon.api.monitoring import metricsclient

LOG = logging.getLogger(__name__)


class PanelView(views.APIView):
    def __init__(self):
        super(PanelView, self).__init__()
        self.monitorclient = monitorclient()
        self.metricsclient = metricsclient()

    def get(self, request, *args, **kwargs):
        start = request.GET['start']
        end = request.GET['end']
        pclass = request.GET['panel_class']
        host_id = request.GET['host_id']

        (path, sep, name) = pclass.rpartition('.')
        try:
            __import__(path)
            panel_class = getattr(sys.modules[path], name)
        except Exception, e:
            raise Exception("Panel %s could not be loaded: %s" % \
                             (pclass, e))
        
        obj = panel_class(
             request,
             monitor_client=self.monitorclient,
             metrics_client=self.metricsclient
        )
        obj.panel_class_name = \
               str(obj.__class__.__module__ +'.'+ obj.__class__.__name__)
        obj.host_id = host_id
        obj.start = start
        obj.end = end
        time.sleep(5)
        return HttpResponse(obj.render(), mimetype="text/html")
