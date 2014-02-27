from django.db import models

class Policy(models.Model):
    id = models.CharField()
    name = models.CharField()
    repo = models.CharField()
    installer = models.CharField()
    broker = models.CharField()
    hostname = models.CharField()
    root_password = models.CharField()
    max_count = models.CharField()
    rule_number = models.CharField()
    tags = models.CharField()
    enabled = models.BooleanField()
  
    def __init__(self,name, repo, installer,broker,hostname,root_password,max_count,rule_number,tags,enabled):
        self.id = name
        self.name=name
        self.repo = repo 
        self.installer =installer 
        self.broker = broker
        self.hostname = hostname
        self.root_password = root_password
        self.max_count = max_count
        self.rule_number = rule_number
        self.tags = tags
        self.enabled = enabled

	def get(self,**kwargs):
		return self