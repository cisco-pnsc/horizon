import logging
import sys

from django.conf import settings
from horizon.api.monitoring.monitor_plugin_base import MonitorPluginBase
from horizon.api.monitoring.metrics_plugin_base import MetricsPluginBase

LOG=logging.getLogger(__name__)

def monitorclient():
    instance = Monitor()
    return instance.client()

def metricsclient():
    instance = Metrics()
    return  instance.client()

def _import_module(mod_str, ref_mod):
        (path, sep, name) = mod_str.rpartition('.')
        try:
            __import__(path)
            plugin_class = getattr(sys.modules[path], name)
        except Exception, e:
            raise Exception("Plugin %s could not be loaded: %s" % \
                             (mod_str, e))

        if not issubclass(plugin_class, ref_mod):
            raise Exception("Configured plugin didn't pass compatibility test")
        else:
            LOG.debug("Successfully imported plugin")
            return plugin_class

class Monitor(object):
    def __init__(self, options=None):
        if not options:
            options = {}

        if settings.MONITOR_OPTIONS:
            options = settings.MONITOR_OPTIONS

        self.options = options
        self.plugin = _import_module(settings.MONITOR_PLUGIN, 
                                     MonitorPluginBase)


    def client(self, *args, **kwargs):
        plugin = self.plugin
        
        return plugin(self.options)

class Metrics(object):
    def __init__(self, options=None):
        if not options:
            options = {}
        
        if settings.METRICS_OPTIONS:
            options = settings.METRICS_OPTIONS
        
        self.options = options
        self.plugin = _import_module(settings.METRICS_PLUGIN,
                                     MetricsPluginBase)

    def client(self, *args, **kwargs):
        plugin = self.plugin

        return plugin(self.options)
