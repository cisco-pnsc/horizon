import logging
from django.conf import settings

LOG=logging.getLogger(__name__)

from horizon.api.monitoring.metrics_plugin_base import MetricsPluginBase

class FakeMetricsPlugin(MetricsPluginBase):
    def __init__(self, options=None):
        self.host = options['fakehost']
        visual_opts = options['visual']
        visual_str = ''
        for key,val in visual_opts.iteritems():
            visual_str += '&' + str(key) + '=' + str(val)
        self.visual = visual_str

    def get_cpu_graph(self, id, start=None, end=None):
        cpustr = 'render?target=carbon.agents.c02-b01-a.cpuUsage'
        return self.host + '/' + cpustr + '&' + self.visual


    def get_mem_graph(self, id, start=None, end=None):
        memstr = 'render?target=carbon.agents.c02-b01-a.memUsage'
        return self.host + '/' + memstr + '&' + self.visual

    def get_network_graph(self, id, interface=None, start=None, end=None):
        netstr = 'render?_salt=1339443729.664&target=c02-b01.interface.if_packets.eth0.rx&target=c02-b01.interface.if_packets.eth0.tx'
        return self.host + '/' + netstr + '&' + self.visual

    def get_partition_graph(self, id, part_id, start=None, end=None):
        partstr = 'render?_salt=1339441480.545&target=c02-b01.df.df.root.free&target=c02-b01.df.df.root.used&target=c02-b01.df.df.dev.free&target=c02-b01.df.df.dev.used&target=c02-b01.df.df.opt-stack-data-swift-drives-sdb1.free&target=c02-b01.df.df.opt-stack-data-swift-drives-sdb1.used'
        return self.host + '/' + partstr + '&' + self.visual

    def get_load_graph(self, id, start=None, end=None):
        loadstr = 'render?_salt=1339442259.041&target=c02-b01.load.load.shortterm&target=c02-b01.load.load.midterm&target=c02-b01.load.load.longterm'
        return self.host + '/' + loadstr + '&' + self.visual

    def get_additional_graphs(self, id):
        pass

    def get_graph(self, id, graph_id, start=None, end=None):
        pass
