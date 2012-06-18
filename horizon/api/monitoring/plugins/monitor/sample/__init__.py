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

    def get_mem_usage(self, id):
        return random.randrange(10, 100)

    def get_errors(self, id):
        errors = []
        return errors

    def get_warnings(self, id):
        warnings = []
        return warnings

    def get_notices(self, id):
        notices = []
        return notices

    def get_services(self, id):
        services  = (
            'compute',
            'network',
            'volumes',
            'storage',
            'api',
            'image'
        )
        return services

    def get_service_status(self, id, service_id):
        states = [-1,0,1]
        return random.choice(states)

    def get_cpu_cores(self, id):
        return [0, 1, 2, 3, 4, 5, 6, 7]

    def get_cpu_speed(self, id, core=None):
        return '3.4'

    def get_total_memory(self, id):
        return 24

    def get_monitored_partitions(self, id):
        return ('/','/var','/var/tmp','/usr','/home')

    def get_partition_stats(self, id, part_id):
        part_size = random.randrange(100, 1000)
        part_used_percent = random.randrange(10, 100)

        part_used = (part_used_percent / 100) * part_size
       
        return { 'total': part_size, 'used': part_used }

    def get_physical_disks(self, id):
        return [
            'sda',
            'sdb',
            'sdc'
        ]

    def get_disk_io(self, id, disk_id):
        return {
            'tps': 3.14,
            'kb_read': 379017,
            'kb_written': 45091052,
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
