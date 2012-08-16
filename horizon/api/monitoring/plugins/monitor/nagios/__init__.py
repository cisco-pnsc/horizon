import logging
import urllib

LOG=logging.getLogger(__name__)

from horizon.api.monitoring.monitor_plugin_base import MonitorPluginBase

class NagiosMonitorPlugin(MonitorPluginBase):
    def __init__(self, options=None):
        self.host = options['host']
        self.port = options['port']

    def _get_state(self):
        url = self.host + ':' + self.port + '/objects'
        res = urllib.urlopen(url)

        data = res.read()
        data = data.replace('true','True')
        data = eval(data)
        
        return data

    def get_monitored_hosts(self):
        data = self._get_state()

        hosts = data['content'].keys()

    def get_overall_state(self, id):
        data = self._get_state()
        state = data['content'][id]['current_state']

        return state

    def get_cpu_load(self, id):
        data = self._get_state()

    def get_cpu_cored(self, id):
        data = self._get_state()

    def get_cpu_speed(self, id):
        data = self._get_state()

    def get_memory(self, id):
        data = self._get_state()

    def get_mem_modules(self, id):
        data = self._get_state()

    def get_mem_usage(self, id):
        data = self._get_state()
