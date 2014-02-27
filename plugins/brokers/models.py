from django.db import models

class Broker(models.Model):
	name = models.CharField()
	id = models.CharField()
	configuration_server = models.CharField()
	configuration_version = models.CharField()
	broker_type = models.CharField()

	def __init__(self,name,configuration_server,configuration_version,broker_type):
		self.name = name
		self.id = name
		self.configuration_server = configuration_server
		self.configuration_version = configuration_version
		self.broker_type = broker_type

	def get(self,**kwargs):
		return self