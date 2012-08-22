import inspect
from abc import ABCMeta, abstractmethod

class MonitorPluginBase(object):
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_hosts(self):
        pass

    @abstractmethod
    def get_host_state(self, host_id):
        pass

    @abstractmethod
    def get_panels(self):
        pass
