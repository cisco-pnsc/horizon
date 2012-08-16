# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.utils.translation import ugettext_lazy as _

from horizon import api
from horizon import exceptions
from horizon import tabs

from horizon.api.monitoring import monitorclient
from horizon.api.monitoring import metricsclient

class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = ("nova/instances/"
                     "_detail_overview.html")

    def get_context_data(self, request):
        return {"instance": self.tab_group.kwargs['instance']}


class LogTab(tabs.Tab):
    name = _("Log")
    slug = "log"
    template_name = "nova/instances/_detail_log.html"
    preload = False

    def get_context_data(self, request):
        instance = self.tab_group.kwargs['instance']
        try:
            data = api.server_console_output(request,
                                            instance.id,
                                            tail_length=35)
        except:
            data = _('Unable to get log for instance "%s".') % instance.id
            exceptions.handle(request, ignore=True)
        return {"instance": instance,
                "console_log": data}


class VNCTab(tabs.Tab):
    name = _("VNC")
    slug = "vnc"
    template_name = "nova/instances/_detail_vnc.html"
    preload = False

    def get_context_data(self, request):
        instance = self.tab_group.kwargs['instance']
        try:
            console = api.nova.server_vnc_console(request, instance.id)
            vnc_url = "%s&title=%s(%s)" % (console.url,
                                           getattr(instance, "name", ""),
                                           instance.id)
        except:
            vnc_url = None
            exceptions.handle(request,
                              _('Unable to get VNC console for '
                                'instance "%s".') % instance.id)
        return {'vnc_url': vnc_url, 'instance_id': instance.id}

class MonitorTab(tabs.Tab):
    name = _("Performance")
    slug = "monitor"
    template_name = "nova/instances_and_volumes/instances/_monitor.html"
    preload = False

    def __init__(self, tab_group, request=None):
        super(MonitorTab, self).__init__(tab_group, request)
        self.monitorclient = monitorclient()
        self.metricsclient = metricsclient()

    def get_context_data(self, request):
        instance = self.tab_group.kwargs['instance']
        panels = []
        panel_list = self.monitorclient.get_panels()
        for panel in panel_list:
            obj = panel(
                self.request,
                monitor_client=self.monitorclient,
                metrics_client=self.metricsclient)
            panels.append(obj)


        graphs = []
        graph_list = self.metricsclient.get_graphs()
        for graph in graph_list:
            obj = graph(
                self.request,
                monitor_client=self.monitorclient,
                metrics_client=self.metricsclient)
            graphs.append(obj)

        return {'panels': panels, 'graphs': graphs} 

class InstanceDetailTabs(tabs.TabGroup):
    slug = "instance_details"
<<<<<<< HEAD:horizon/dashboards/nova/instances_and_volumes/instances/tabs.py
    tabs = (OverviewTab, LogTab, VNCTab, MonitorTab)
=======
    tabs = (OverviewTab, LogTab, VNCTab)
    sticky = True
>>>>>>> master:horizon/dashboards/nova/instances/tabs.py
