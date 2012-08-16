import logging
import random

from horizon.api.monitoring.monitor_plugin_base import MonitorPluginBase
from horizon.panels import Panel, LoadPanel, ServicePanel, NoticePanel

LOG=logging.getLogger(__name__)


class FakeMonitorPlugin(MonitorPluginBase):
    def __init__(self, options=None):
        self.monitor_host = options['host']
        self.monitor_port = options['port']

    def get_hosts(self):
        hosts = (
            {'name': '64.102.251.78', 'state': 'OK', 'class':'host_ok'},
            {'name': '64.102.251.79', 'state': 'WARNING', 'class':'host_warn'}
        )
        return hosts
    
    def get_panels(self):
        return (errors, warnings, notices, cpu, memory,
                network, users, processes, services)

class errors(NoticePanel):
    label = 'Errors'
    icon = '/media/dashboard/img/error.png'
    panel_class = 'important'

    def get_data(self): 
        return (
            'Fan 2 failed',
            'CPU1 shutdown due to overheating'
        )

class warnings(NoticePanel):
    label = 'Warnings'
    icon = '/media/dashboard/img/warning.png'
    panel_class = 'warning'

    def get_data(self): 
        return (
            'Disk1 storage 90% full',
            'CPU2 overheating'
        )

class notices(NoticePanel):
    label = 'Notices'
    icon = '/media/dashboard/img/notice.png'
    panel_class = 'info'

    def get_data(self):
        return (
            'System reboot at 10:00 UTC',
            'BIOS reconfigured at 10:01 UTC'
        )

class cpu(LoadPanel):
    label = 'CPU'
    icon = '/media/dashboard/img/cpu.png'
    load_label = 'Cpu Load'
    load_suffix = '%'

    def get_load(self):
        cpu.load_class = 'warning'
        return 80

    def get_data(self):
        load = random.randrange(10, 100)

        return (
            {'Cores': 8},
            {'Speed/Core': '3.4Ghz'},
            {'Load': self.get_load()}
        )


class memory(LoadPanel):
    label = 'Memory'
    icon = '/media/dashboard/img/mem.png'
    load_label = 'Memory Usage'
    load_suffix = '%'

    def get_load(self):
        return 60

    def get_data(self):
        total = '24 GB'
        used = '14.4 GB'
        free = '9.6 GB'
        
        return (
            {'Total Memory': total},
            {'Free': free},
            {'Used': used}
        )

class network(LoadPanel):
    label = 'Network'
    icon = '/media/dashboard/img/net.png'
    load_label = 'Traffic'
    load_suffix = '%'

    def get_load (self):
        return 50

    def get_data(self):
        total = '10 Gbps'
        used = '5 Gbps'
        free = '5 Gbps'
        
        return (
            {'Total Bandwidth': total},
            {'Traffic': used},
            {'Free': free}
        )

class users(Panel):
    label = 'Users'
    icon = '/media/dashboard/img/users.png'

    def get_data(self):
        users = random.randrange(100, 300)
        uusers = random.randrange(100,200)

        return (
            {'Current Users': users},
            {'Unique Users': uusers}
        )

class processes(Panel):
    label = 'Processes'
    icon = '/media/dashboard/img/processes.png'

    def get_data(self):
        processes = random.randrange(500, 1000)
        forks = random.randrange(100,200)
        orphans = random.randrange(50,80)
        zombies = random.randrange(50,80)

        return (
            {'Current Processes': processes},
            {'Forks': forks},
            {'Orphans': orphans},
            {'Zombies': zombies}
        )

class services(Panel):
    label = 'Services'
    icon = '/media/dashboard/img/service.png'

    def get_data(self):
        return (
            {'Glance': 'OK'},
            {'Keystone': 'OK'},
            {'Nova API': 'OK'},
            {'SSH': 'OK'},
            {'RabbitMQ': 'OK'},
            {'RabbitMQ Server': 'OK'},
            {'HTTP': 'OK'},
        )
