<<<<<<< HEAD
# Copyright 2012 Cisco Systems, Inc.
=======
# Copyright 2012 Nebula, Inc.
>>>>>>> master
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
<<<<<<< HEAD
from horizon.api import quantum
from horizon.api import nova

from novaclient.v1_1 import servers
=======

import copy

from horizon.api.quantum import Network, Subnet, Port
>>>>>>> master

from .utils import TestDataContainer


def data(TEST):
<<<<<<< HEAD
    TEST.networks = {}
    TEST.network_details = {}
    TEST.ports = {}
    TEST.port_details = {}
    TEST.network_list = []
    TEST.port_list = []
    TEST.instance_interfaces = []

    # Networks
    networks = [{'id': u'5d3ad338-4aea-4f97-a4d8-ad9488da9b49'}]

    networks_dict = {'name': u'private',
                     'id': u'5d3ad338-4aea-4f97-a4d8-ad9488da9b49',
                    }
    network = quantum.Network(networks_dict)
    TEST.networks['networks'] = networks
    TEST.network_details['network'] = networks_dict
    TEST.network_list.append(network)

    # Ports
    ports = [{'id': u'96e9652d-6bdb-4c20-8d79-3eb823540298'}]
    TEST.ports['ports'] = ports

    port_details = {'id': u'96e9652d-6bdb-4c20-8d79-3eb823540298',
                    'state': 'DOWN',
                    'op-state': 'DOWN'
                   }
    TEST.port_details['port'] = port_details

    test_port = {'id':  u'96e9652d-6bdb-4c20-8d79-3eb823540298',
                 'state': 'DOWN',
                 'op-state': 'DOWN',
                 'attachment_id': '1',
                 'attachment_server': 'vm1'
                }
    port = quantum.Port(test_port)
    TEST.port_list.append(port)

    # Attachment
    TEST.port_attachment = {}
    port_attachment = {'id': 'vif1'}
    TEST.port_attachment['attachment'] = port_attachment

    # Instances
    TEST.instances = []
    instance = {'id': '1', 'name': 'instance1'}
    instance_1 = servers.Server(servers.ServerManager(None), instance)
    TEST.instances.append(instance_1)

    # Vifs
    TEST.vifs = []
    vif = {'id': 'vif1'}
    vif_1 = quantum.Vif(vif)

    TEST.vifs.append(vif_1)

    instance_vif = {
                    'instance': 'vm1',
                    'vif': vif_1.id
                   }
    TEST.instance_interfaces.append(instance_vif)
=======
    # data returned by horizon.api.quantum wrapper
    TEST.networks = TestDataContainer()
    TEST.subnets = TestDataContainer()
    TEST.ports = TestDataContainer()

    # data return by quantumclient
    TEST.api_networks = TestDataContainer()
    TEST.api_subnets = TestDataContainer()
    TEST.api_ports = TestDataContainer()

    # 1st network
    network_dict = {'admin_state_up': True,
                    'id': '82288d84-e0a5-42ac-95be-e6af08727e42',
                    'name': 'net1',
                    'status': 'ACTIVE',
                    'subnets': ['e8abc972-eb0c-41f1-9edd-4bc6e3bcd8c9'],
                    'tenant_id': '1'}
    subnet_dict = {'allocation_pools': [{'end': '10.0.0.254',
                                         'start': '10.0.0.2'}],
                   'cidr': '10.0.0.0/24',
                   'enable_dhcp': True,
                   'gateway_ip': '10.0.0.1',
                   'id': network_dict['subnets'][0],
                   'ip_version': 4,
                   'name': 'mysubnet1',
                   'network_id': network_dict['id'],
                   'tenant_id': network_dict['tenant_id']}
    port_dict = {'admin_state_up': True,
                 'device_id': 'af75c8e5-a1cc-4567-8d04-44fcd6922890',
                 'fixed_ips': [{'ip_address': '10.0.0.3',
                                'subnet_id': subnet_dict['id']}],
                 'id': '3ec7f3db-cb2f-4a34-ab6b-69a64d3f008c',
                 'mac_address': 'fa:16:3e:9c:d5:7e',
                 'name': '',
                 'network_id': network_dict['id'],
                 'status': 'ACTIVE',
                 'tenant_id': network_dict['tenant_id']}

    TEST.api_networks.add(network_dict)
    TEST.api_subnets.add(subnet_dict)
    TEST.api_ports.add(port_dict)

    network = copy.deepcopy(network_dict)
    subnet = Subnet(subnet_dict)
    network['subnets'] = [subnet]
    TEST.networks.add(Network(network))
    TEST.subnets.add(subnet)
    TEST.ports.add(Port(port_dict))

    # 2nd network
    network_dict = {'admin_state_up': True,
                    'id': '72c3ab6c-c80f-4341-9dc5-210fa31ac6c2',
                    'name': 'net2',
                    'status': 'ACTIVE',
                    'subnets': ['3f7c5d79-ee55-47b0-9213-8e669fb03009'],
                    'tenant_id': '2'}
    subnet_dict = {'allocation_pools': [{'end': '172.16.88.254',
                                          'start': '172.16.88.2'}],
                   'cidr': '172.16.88.0/24',
                   'enable_dhcp': True,
                   'gateway_ip': '172.16.88.1',
                   'id': '3f7c5d79-ee55-47b0-9213-8e669fb03009',
                   'ip_version': 4,
                   'name': 'aaaa',
                   'network_id': network_dict['id'],
                   'tenant_id': network_dict['tenant_id']}
    port_dict = {'admin_state_up': True,
                 'device_id': '40e536b1-b9fd-4eb7-82d6-84db5d65a2ac',
                 'fixed_ips': [{'ip_address': '172.16.88.3',
                                'subnet_id': subnet_dict['id']}],
                 'id': '7e6ce62c-7ea2-44f8-b6b4-769af90a8406',
                 'mac_address': 'fa:16:3e:56:e6:2f',
                 'name': '',
                 'network_id': network_dict['id'],
                 'status': 'ACTIVE',
                 'tenant_id': network_dict['tenant_id']}

    TEST.api_networks.add(network_dict)
    TEST.api_subnets.add(subnet_dict)
    TEST.api_ports.add(port_dict)

    network = copy.deepcopy(network_dict)
    subnet = Subnet(subnet_dict)
    network['subnets'] = [subnet]
    TEST.networks.add(Network(network))
    TEST.subnets.add(subnet)
    TEST.ports.add(Port(port_dict))
>>>>>>> master
