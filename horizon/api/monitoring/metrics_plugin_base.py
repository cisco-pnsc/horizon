import inspect
from abc import ABCMeta, abstractmethod

class MetricsPluginBase(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_cpu_graph(self, id, core=None, start=None, end=None):
        pass

    @abstractmethod
    def get_mem_graph(self, id, module=None, start=None, end=None):
        pass

    @abstractmethod
    def get_network_graph(self, id, interface=None, start=None, end=None):
        pass

    @abstractmethod
    def get_partition_graph(self, id, partition=None, start=None, end=None):
        pass

    @abstractmethod
    def get_additional_graphs(self, id):
        pass

    @abstractmethod
    def get_graph(self, id, graph_id, start=None, end=None):
        pass
