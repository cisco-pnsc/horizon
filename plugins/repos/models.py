from django.db import models

class Repo(models.Model):
	name = models.CharField()
	id = models.CharField()
	iso_url = models.CharField()
	
	def __init__(self,name,iso_url):
		self.name = name
		self.id = name
		self.iso_url = iso_url

	def get(self,**kwargs):
		return self