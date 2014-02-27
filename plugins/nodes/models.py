from django.db import models

class Node(models.Model):
	name = models.CharField()
	id = models.CharField()
	status = models.CharField()
	ipaddress = models.CharField()
	log_link = models.CharField()
	policy = models.CharField()
	tags = models.CharField()
	spec = models.CharField()

	def __init__(self,name,spec,status,ipaddress="",log_link="",policy="",tags=""):
		self.id = name
		self.name = name
		self.status = status
		self.ipaddress = ipaddress
		self.log_link = log_link
		self.policy = policy
		self.tags = tags
		self.spec = spec

	def get(self,**kwargs):
		return self