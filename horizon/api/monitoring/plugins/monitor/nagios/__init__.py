import logging
import urllib
import re

from horizon.api.monitoring.monitor_plugin_base import MonitorPluginBase
from horizon.panels import Panel, LoadPanel, MultiLoadPanel, ServicePanel, NoticePanel

LOG=logging.getLogger(__name__)


class NagiosPlugin(MonitorPluginBase):
    def __init__(self, options=None):
        self.monitor_host = options['host']
        self.monitor_port = options['port']

    def _get_state(self):
        url = self.monitor_host + ':' + str(self.monitor_port) + '/state'
        res = urllib.urlopen(url)

        data = res.read()
        data = data.replace('true','True')
        data = eval(data)

        return data

    def get_hosts(self):
        objects = self._get_state()
        hosts = []
        state = 0
        host_class = ''

        for key in objects['content']:
            state = objects['content'][key]['current_state']
            if int(state) == 0:
                state = 'OK'
                host_class = 'host_ok'
            elif int(state) == 1:
                state = 'WARNING'
                host_class = 'host_warn'
            else:
                state = 'ERROR'
                host_class = 'host_error'
            hosts.append({'name': key, 'state': state, 'class': host_class})

        return hosts
   
    def get_host_state(self, host_id):
        hosts = self.get_hosts()
        for host in hosts:
            if host['name'] == host_id:
                return host['state']

        return 'Unknown'

    def get_panels(self):
        return (services, load, vmcpu)

    def get_services(self):
        services = []
        data = self._get_state()

        for host in data['content'].keys():
            for service in data['content'][host]['services'].keys():
                service_dict = data['content'][host]['services'][service]
                status = ''
                if int(service_dict['current_state']) == 0:
                    status = 'OK'
                elif int(service_dict['current_state']) == 1:
                    status = 'WARNING'
                else:
                    status = 'ERROR'

                services.append({
                    'name': service, 'status': status, 'host': host
                })

        return services

class services(Panel):
    label = 'Services'
    icon = '/media/dashboard/img/service.png'

    def get_data(self):
        services = []
        data = self.monitor_client()._get_state()
        service_dict = data['content'][self.host_id]['services']

        for service in service_dict.keys():
            status = ''
            if int(service_dict[service]['current_state']) == 0:
                status = 'OK'
            elif int(service_dict[service]['current_state']) == 1:
                status = 'WARNING'
            else:
                status = 'ERROR'
                
            services.append({service: status})

        return services

class load(MultiLoadPanel):
    label = 'Load'
    icon = '/media/dashboard/img/load.png'

    def get_loads(self):
        loads = []
        data = self.monitor_client()._get_state()
        cload_str = data['content'][self.host_id]['services']['Current Load']['plugin_output']
        load_floats = re.findall("\d+.\d+", cload_str)
        for load in load_floats:
            lclass = 'success'
            if float(load) > float(0.90):
                lclass = 'danger'
            elif float(load) > float(0.70):
                lclass = 'warning'

            loads.append({
                'load_label':'Load Average',
                'load_value': float(load) * 100,
                'load_suffix': '%',
                'load_class': lclass
            })
        return loads
        
    def get_data(self):
        pass

class vmcpu(MultiLoadPanel):
    label = 'VM Stats'
    icon = '/media/dashboard/img/vm.png'

    def get_loads(self):
        loads = []
        data = self.monitor_client()._get_state()
        vload_str = data['content'][self.host_id]['services']['VM CPU and Memory']['plugin_output']
        vload_str = re.sub('^[a-zA-Z]+\s+-\s+Instance:', '', vload_str)
        vload_str = re.sub(r'\s', '', vload_str)
        vload_str = re.sub(r'%', '', vload_str)
        vload_str = re.sub(r'CPU:', '', vload_str)
        vload_str = re.sub(r'Memory:', '', vload_str)
        vm_strs = vload_str.split('Instance:')
        if not re.match(',', vm_strs):
            vm_strs = []

        for vm in vm_strs:
            stats = vm.split(',')
            name = stats[0]
            cpu = stats[2]
            mem = stats[3]
            lclass = 'success'

            loads.append({
                'load_label': name + ' CPU',
                'load_value': cpu,
                'load_suffix': '%',
                'load_class': lclass
            })
            loads.append({
                'load_label': name + ' Memory',
                'load_value': mem,
                'load_suffix': '%',
                'load_class': lclass
            })
        return loads

    def get_data(self):
        pass
