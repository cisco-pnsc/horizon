import logging
from datetime import datetime, timedelta

from django import template
from django.core.urlresolvers import reverse

import urls

LOG = logging.getLogger(__name__)


class Panel(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.monitor_client = kwargs['monitor_client']
        self.metrics_client = kwargs['metrics_client']
        self.template = 'horizon/common/_panel.html'
        self.host_id = False
        self.url = reverse('index')

    def render(self):
        templ = template.loader.get_template(self.template)
        context = template.RequestContext(self.request, {'panel': self})
        return templ.render(context)

    def get_data(self):
        pass


class LoadPanel(Panel):
    load_class = 'success'

    def __init__(self, request, *args, **kwargs):
        super(LoadPanel, self).__init__(request, *args, **kwargs)
        self.template = 'horizon/common/_load_panel.html'

    def get_load(self):
        pass


class MultiLoadPanel(Panel):
    def __init__(self, request, *args, **kwargs):
        super(MultiLoadPanel, self).__init__(request, *args, **kwargs)
        self.template = 'horizon/common/_multi_load_panel.html'

    def get_loads(self):
        pass

class ServicePanel(Panel):
    def __init__(self, request, *args, **kwargs):
        super(ServicePanel, self).__init__(request, *args, **kwargs)
        self.template = 'horizon/common/_service_panel.html'


class GraphPanel(Panel):
    def __init__(self, request, *args, **kwargs):
        super(GraphPanel, self).__init__(request, *args, **kwargs)
        self.template = 'horizon/common/_graph_panel.html'
        # Calculate 24 hours as default start and stop
        self.end = datetime.now()
        self.start = self.end - timedelta(days=1)
        self.end = self.end.strftime("%m/%d/%y")
        self.start = self.start.strftime("%m/%d/%y")

    def get_graph(self):
        pass


class NoticePanel(Panel):
    def __init__(self, request, *args, **kwargs):
        super(NoticePanel, self).__init__(request, *args, **kwargs)
        self.template = 'horizon/common/_notice_panel.html'
