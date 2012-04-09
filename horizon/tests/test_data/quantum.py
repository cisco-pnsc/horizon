# Copyright 2012 Cisco Systems, Inc.
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
from horizon.api import quantum
from .utils import TestDataContainer

def data(TEST):
    TEST.networks = TestDataContainer()
    TEST.ports = TestDataContainer()

    # Networks
    networks_dict = { 'name': u'private',
                      'id' : u'5d3ad338-4aea-4f97-a4d8-ad9488da9b49',
                      'port_count': 2
                    }
    network = quantum.Network(networks_dict)
    TEST.networks.add(network)

    # Ports
    port_dict = { 'id': u'96e9652d-6bdb-4c20-8d79-3eb823540298',
                  'attachment_server': u'Instance1',
                  'attachment_id': 1,
                  'state': 'DOWN',
                  'op-state': 'DOWN'
                }
    port1 = quantum.Port(port_dict)
 
    port_dict = { 'id': u'f855136f-8fba-4b3f-ba73-cc6a7f195c7c',
                  'attachment_server': u'Instance2',
                  'attachment_id': 2,
                  'state': 'ACTIVE',
                  'op-state': 'ACTIVe'
                }
    port2 = quantum.Port(port_dict)
    TEST.ports.add(port1, port2)
