import inspect
from abc import ABCMeta, abstractmethod

class MonitorPluginBase(object):
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_overall_state(self, id):
        pass

    @abstractmethod
    def get_cpu_load(self, id, core=None):
        pass

    @abstractmethod
    def get_cpu_cores(self, id):
        pass

    @abstractmethod
    def get_cpu_speed(self, id, core=None):
        pass

    @abstractmethod
    def get_memory(self, id, module_id=None):
        pass

    @abstractmethod
    def get_memory_modules(self, id):
        pass

    @abstractmethod
    def get_mem_usage(self, id, module_id=None):
        pass

    @abstractmethod
    def get_monitored_partitions(self, id):
        pass

    @abstractmethod
    def get_partition_stats(self, id, part_id):
        pass

    @abstractmethod
    def get_errors(self, id):
        pass

    @abstractmethod
    def get_warnings(self, id):
        pass

    @abstractmethod
    def get_notices(self, id):
        pass

    @abstractmethod
    def get_services(self, id):
        pass

    @abstractmethod
    def get_service_status(self, id, service_id):
        pass

    @abstractmethod
    def get_physical_disks(self, id):
        pass

    @abstractmethod
    def get_disk_io(self, id, disk_id):
        pass

    @abstractmethod
    def get_monitored_interfaces(self, id):
        pass

    @abstractmethod
    def get_interface_stats(self, id, interface_id):
        pass
