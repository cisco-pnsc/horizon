import logging
import random

LOG=logging.getLogger(__name__)

from horizon.api.monitoring.monitor_plugin_base import MonitorPluginBase

class FakeMonitorPlugin(MonitorPluginBase):
    def __init__(self, options=None):
        pass

    def get_overall_state(self, id):
        states = [-1,0,1]
        return random.choice(states)

    def get_cpu_load(self, id, core=None):
        return random.randrange(10, 100)

    def get_mem_usage(self, id, module_id=None):
        return random.randrange(10, 100)

    def get_errors(self, id):
        errors = [
            'Fan module 2 failed',
            'Fan tray 2 sensor unresponsive',
            'Fan module 2 failed',
            'Fan tray 2 sensor unresponsive',
            'Fan module 2 failed',
            'Fan tray 2 sensor unresponsive',
            'Fan module 2 failed',
            'Fan tray 2 sensor unresponsive',
            'Fan module 2 failed',
            'Fan tray 2 sensor unresponsive',
            'Fan module 2 failed',
            'Fan tray 2 sensor unresponsive',
            'Fan module 2 failed',
            'Fan tray 2 sensor unresponsive',
            'Fan module 2 failed',
            'Fan tray 2 sensor unresponsive',
            'Fan module 2 failed',
            'Fan tray 2 sensor unresponsive',
            'Fan module 2 failed',
            'Fan tray 2 sensor unresponsive'
        ]
        return errors

    def get_warnings(self, id):
        warnings = [
            'CPU temperature high',
            'CPU load high',
            'CPU temperature high',
            'CPU load high',
            'CPU temperature high',
            'CPU load high',
            'CPU temperature high',
            'CPU load high',
            'CPU temperature high',
            'CPU load high',
            'CPU temperature high',
            'CPU load high',
            'CPU temperature high',
            'CPU load high',
            'CPU temperature high',
            'CPU load high',
        ]
        return warnings

    def get_notices(self, id):
        notices = [
            'System rebooted at 00:00:00',
            'Config backed up at 00:00:00',
            'System rebooted at 00:00:00',
            'Config backed up at 00:00:00',
            'System rebooted at 00:00:00',
            'Config backed up at 00:00:00',
            'System rebooted at 00:00:00',
            'Config backed up at 00:00:00',
            'System rebooted at 00:00:00',
            'Config backed up at 00:00:00',
            'System rebooted at 00:00:00',
            'Config backed up at 00:00:00',
            'System rebooted at 00:00:00',
            'Config backed up at 00:00:00',
            'System rebooted at 00:00:00',
            'Config backed up at 00:00:00',
        ]
        return notices

    def get_services(self, id):
        services  = {
          'compute': 'compute',
          'network': 'network',
          'volumes': 'volumes',
          'swift': 'swift',
          'api': 'api',
          'image': 'image',
          'rabbitmq': 'rabbitmq',
          'mysql': 'mysql',
          'glance': 'glance',
        }
        return services

    def get_service_status(self, id, service_id):
        states = [-1,0,1]
        return random.choice(states)

    def get_cpu_cores(self, id):
        return [0, 1, 2, 3, 4, 5, 6, 7]

    def get_cpu_speed(self, id, core=None):
        return '3.4'

    def get_memory(self, id, module_id=None):
        if module_id:
            return 4
        else:
            return 16

    def get_memory_modules(self, id):
        return ['dimm0','dimm1','dimm2','dimm3','dimm4',
                'dimm5','dimm6','dimm7']
    
    def get_monitored_partitions(self, id):
        return ('root','dev','opt-stack-data','usr','home')

    def get_partition_stats(self, id, part_id):
        part_size = random.randrange(100, 1000)
        part_used_percent = random.randrange(10, 100)

        return { 'size': part_size, 'used_percent': part_used_percent }

    def get_physical_disks(self, id):
        return ['sda', 'sdb', 'sdc', 'sdd']

    def get_disk_io(self, id, disk_id):
        return {
            'tps': 3.14,
            'kb_read': random.randrange(20000, 50000),
            'kb_written': random.randrange(400000, 500000),
        }

    def get_monitored_interfaces(self, id):
        return ['eth0','eth1','eth2']

    def get_interface_stats(self, id, interface_id):
        rx = random.randrange(10000, 1000000)
        tx = random.randrange(10000, 1000000)
        bandwidth = random.choice([100,1000,10000])
        used = random.randrange(1, 100)

        return  {
            'rx': rx,
            'tx': tx,
            'bandwidth': bandwidth,
            'used': used
        }
