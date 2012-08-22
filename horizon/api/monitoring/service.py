from horizon.api import base

class Service(base.APIDictWrapper):
     _attrs = ['id', 'name', 'status', 'host']
