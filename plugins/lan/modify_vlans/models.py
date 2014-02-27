from django.db import models

class Profile(models.Model):

    id = models.CharField()
    name = models.CharField()
    type = models.CharField()
    
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type


class Nic(models.Model):
    
    id = models.CharField()
    name = models.CharField()
    
    def __init__(self, id, name):
        self.id = id
        self.name = name