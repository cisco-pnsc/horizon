import inspect
from abc import ABCMeta, abstractmethod

class MetricsPluginBase(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_graphs(self, host_id):
        pass
