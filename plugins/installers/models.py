from django.db import models
import ast

class Installer(models.Model):
    id = models.CharField()
    name = models.CharField()
    os = models.CharField()
    os_version = models.CharField()
    description = models.CharField()
    boot_seq = {}
    templates = {}
    
    def __init__(self,name,os,os_version,description,boot_seq,templates):
        self.name=name
        self.id=name
        self.os= os
        self.os_version=os_version
        self.description=description
        self.boot_seq= ast.literal_eval(boot_seq).copy()
        self.templates = ast.literal_eval(templates).copy() 

	def get(self,**kwargs):
		return self