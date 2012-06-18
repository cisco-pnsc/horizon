import logging
from django.conf import settings

LOG=logging.getLogger(__name__)

class MetricsManager(object):
    def __init__(self, options=None):
        if not options:
            options = {}
