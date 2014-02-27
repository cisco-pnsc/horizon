from django.db import models

class Server(models.Model):
    name = models.CharField()
    id = models.CharField()
    chassis = models.CharField()
    slot = models.CharField()
    cpu = models.IntegerField()
    ram = models.CharField()
    associate = models.BooleanField()
    on = models.CharField()
    state = models.CharField() 
        
    def __init__(self,id,name,chassis,slot,cpu,ram,associate,on, fsm):
        self.name = name
        self.id = id
        self.chassis = chassis
        self.slot = slot
        self.cpu = cpu
        self.ram = ram
        self.associate = associate
        self.on = on
        self.state = fsm
