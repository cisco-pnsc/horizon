import logging
from django.conf import settings

from horizon.api.monitoring.metrics_plugin_base import MetricsPluginBase
from horizon.panels import Panel, GraphPanel

LOG=logging.getLogger(__name__)

def _visual_str(options):
    visual_opts = options['visual']
    visual_str = ''
    for key,val in visual_opts.iteritems():
        visual_str += '&' + str(key) + '=' + str(val)
    return visual_str


class FakeMetricsPlugin(MetricsPluginBase):
    def __init__(self, options=None):
        self.host = options['fakehost']
        self.visual = _visual_str(options)
        
    def get_graphs(self):
        return (cpu, memory, network, load) 


class cpu(GraphPanel):
    label = 'CPU Graph'
    date_select = True

    def get_graph(self):
        cpustr = 'render?target=carbon.agents.c02-b01-a.cpuUsage'
        return self.metrics_client().host +\
               '/' + cpustr + '&' + self.metrics_client().visual

class memory(GraphPanel):
    label = 'Memory Graph'
    date_select = True
    
    def get_graph(self):
        memstr = 'render?target=carbon.agents.c02-b01-a.memUsage'
        return self.metrics_client().host +\
               '/' + memstr + '&' + self.metrics_client().visual

class network(GraphPanel):
    label = 'Network Graph'
    date_select = True
    
    def get_graph(self):
        netstr = 'render?_salt=1339443729.664&target=c02-b01.interface.if_packets.eth0.rx&target=c02-b01.interface.if_packets.eth0.tx'
        return self.metrics_client().host +\
               '/' + netstr + '&' + self.metrics_client().visual

class load(GraphPanel):
    label = 'Load'
    date_select = True

    def get_graph(self):
        loadstr = 'render?_salt=1339442259.041&target=c02-b01.load.load.shortterm&target=c02-b01.load.load.midterm&target=c02-b01.load.load.longterm'
        return self.metrics_client().host +\
               '/' + loadstr + '&' + self.metrics_client().visual
