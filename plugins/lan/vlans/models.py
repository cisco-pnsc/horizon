from django.db import models

class VLAN(models.Model):
    name = models.CharField()
    id = models.CharField()
    native = models.BooleanField()
    nw_type = models.CharField()
    locale = models.CharField()
    owner = models.CharField()
    multicast_policy_name = models.CharField()
    multicast_policy_instance = models.CharField()
    sharing_type = models.CharField()
    fabric_id = models.CharField()
    if_type = models.CharField()
    transport_type = models.CharField()

    def __init__(self, id, name,native = False, nw_type='lan', locale='external', owner = 'local', multicast_policy_name = '', multicast_policy_instance = '', sharing_type = 'none', fabric_id = 'dual', if_type = 'virtual', transport_type = 'ether'):  
        self.id = id
        self.name = name
        self.native = native
        self.nw_type = nw_type
        self.locale = locale
        self.owner = owner
        self.multicast_policy_name = multicast_policy_name
        self.multicast_policy_instance = multicast_policy_instance
        self.sharing_type = sharing_type
        self.fabric_id = fabric_id
        self.if_type = if_type
        self.transport_type = transport_type


class MCPolicy(models.Model):

    name = models.CharField()
    id = models.CharField()
    icmp_snooping = models.CharField()
    icmp_snooping_querier = models.CharField()
    
    def __init__(self, name, icmp_snooping, icmp_snooping_querier):
        self.name = name
        self.id = name
        self.icmp_snooping = icmp_snooping
        self.icmp_snooping_querier = icmp_snooping_querier
   
    
        