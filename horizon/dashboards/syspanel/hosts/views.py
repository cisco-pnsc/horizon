import logging
import simplejson

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _

from horizon import views
from horizon.api.monitoring import monitorclient
from horizon.api.monitoring import metricsclient
from horizon import api
from horizon import exceptions
from horizon import tables

LOG = logging.getLogger(__name__)

class HostsView(views.APIView):
    template_name = 'syspanel/hosts/index.html'

    def get_data(self, request, context, *args, **kwargs):
        host_list = {}

        host_list = monitorclient().get_hosts()

        context['hosts'] = host_list
        return context


class HostDetailView(views.APIView):
    template_name = 'syspanel/hosts/details.html'

    def __init__(self):
        super(HostDetailView, self).__init__()
        self.monitorclient = monitorclient
        self.metricsclient = metricsclient

    def get_data(self, request, context, *args, **kwargs):
        host = kwargs['host_id']
        panels = []
        panel_list = self.monitorclient().get_panels()
        for panel in panel_list:
            obj = panel(
                self.request,
                monitor_client=self.monitorclient,
                metrics_client=self.metricsclient)
            obj.panel_class_name = \
               str(obj.__class__.__module__ +'.'+ obj.__class__.__name__)
            obj.host_id = host
            panels.append(obj)

        context['panels'] = panels

        graphs = []
        graph_list = self.metricsclient().get_graphs()
        for graph in graph_list:
            obj = graph(
                self.request,
                monitor_client=self.monitorclient,
                metrics_client=self.metricsclient)
            obj.panel_class_name = \
               str(obj.__class__.__module__ +'.'+ obj.__class__.__name__)
            obj.host_id = host
            graphs.append(obj)

        context['graphs'] = graphs
 
        return context
