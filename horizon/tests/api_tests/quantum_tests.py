# vim: tabstop=4 shiftwidth=4 softtabstop=4

<<<<<<< HEAD
# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Cisco Systems, Inc.
=======
# Copyright 2012 NEC Corporation
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
from quantumclient.common import exceptions as quantum_exceptions

=======
>>>>>>> master
from horizon import api
from horizon import test


class QuantumApiTests(test.APITestCase):
<<<<<<< HEAD
    def test_get_quantumclient(self):
        """ Verify the client connection method does what we expect. """
        # Replace the original client which is stubbed out in setUp()
        api.quantum.quantumclient = self._original_quantumclient

        client = api.quantumclient(self.request)
        self.assertEqual(client.auth_token, self.tokens.first().id)

    def test_quantum_network_list(self):
        networks = self.networks
        network = self.networks['networks'][0]
        network_details = self.network_details
        ports = self.ports

        quantumclient = self.stub_quantumclient()
        quantumclient.list_networks().AndReturn(networks)
        quantumclient.show_network_details(network['id']).\
            AndReturn(network_details)
        quantumclient.list_ports(network['id']).AndReturn(ports)

        self.mox.ReplayAll()

        ret_val = api.quantum_network_list(self.request)
        self.assertIsInstance(ret_val[0], api.quantum.Network)
        self.assertEqual(ret_val[0].id, network['id'])
        self.assertEqual(ret_val[0].name, 'private')
        self.assertEqual(ret_val[0].port_count, 1)

    def test_quantum_network_create(self):
        send_data = {'network': {'name': 'public'}}
        recv_data = {'network':
                        {'name': u'public',
                         'id': u'5d3ad338-4aea-4f97-a4d8-ad9488da9b49'}
                    }

        quantumclient = self.stub_quantumclient()
        quantumclient.create_network(send_data).AndReturn(recv_data)

        self.mox.ReplayAll()

        ret_val = api.quantum_network_create(self.request, 'public')
        self.assertEqual(ret_val['network']['name'], u'public')
        self.assertEqual(
            ret_val['network']['id'],
            u'5d3ad338-4aea-4f97-a4d8-ad9488da9b49')

    def test_quantum_network_delete(self):
        network = self.networks['networks'][0]

        quantumclient = self.stub_quantumclient()
        quantumclient.delete_network(network['id']).\
            AndReturn(True)

        self.mox.ReplayAll()

        ret_val = api.quantum_network_delete(self.request, network['id'])
        self.assertEqual(ret_val, True)

    def test_quantum_port_list(self):
        ports = self.ports
        port_details = self.port_details
        port_attachment = self.port_attachment
        network = self.networks['networks'][0]
        port = self.ports['ports'][0]
        instances = self.instances
        vifs = self.vifs

        quantumclient = self.stub_quantumclient()
        novaclient = self.stub_novaclient()

        quantumclient.list_ports(network['id']).AndReturn(ports)
        quantumclient.show_port_details(
            network['id'], port['id']).AndReturn(port_details)

        quantumclient.show_port_attachment(
            network['id'], port['id']).AndReturn(port_attachment)
        novaclient.servers = self.mox.CreateMockAnything()
        novaclient.servers.list(True, {'project_id': '1'}).\
            AndReturn(instances)
        novaclient.virtual_interfaces = self.mox.CreateMockAnything()
        novaclient.virtual_interfaces.list('1').\
            AndReturn(vifs)

        self.mox.ReplayAll()

        ret_val = api.quantum_port_list(self.request, network['id'])
        self.assertIsInstance(ret_val[0], api.quantum.Port)
        self.assertEqual(ret_val[0].id, port['id'])
        self.assertEqual(ret_val[0].attachment_id, 'vif1')
        self.assertEqual(ret_val[0].attachment_server, 'instance1')

    def test_quantum_port_create(self):
        network = self.networks['networks'][0]

        quantumclient = self.stub_quantumclient()
        quantumclient.create_port(network['id']).AndReturn(True)

        self.mox.ReplayAll()

        ret_val = api.quantum_port_create(self.request, 1, network['id'])
        self.assertEqual(ret_val, None)

    def test_quantum_port_attach(self):
        network = self.networks['networks'][0]
        port = self.ports['ports'][0]
        vif = self.vifs[0]

        quantumclient = self.stub_quantumclient()
        quantumclient.attach_resource(
            network['id'],
            port['id'],
            {'attachment': {'id': vif.id}}).AndReturn(True)

        self.mox.ReplayAll()

        ret_val = api.quantum_port_attach(
            self.request,
            network['id'],
            port['id'],
            vif.id)
        self.assertEqual(ret_val, True)

    def test_quantum_port_delete(self):
        network = self.networks['networks'][0]
        port = self.ports['ports'][0]

        quantumclient = self.stub_quantumclient()
        quantumclient.delete_port(network['id'], port['id']).AndReturn(True)

        self.mox.ReplayAll()

        ret_val = api.quantum_port_delete(
            self.request,
            network['id'],
            port['id'])
        self.assertEqual(ret_val, True)

    def test_quantum_port_detach(self):
        network = self.networks['networks'][0]
        port = self.ports['ports'][0]

        quantumclient = self.stub_quantumclient()
        quantumclient.detach_resource(
            network['id'],
            port['id']).AndReturn(True)

        self.mox.ReplayAll()

        ret_val = api.quantum_port_detach(
            self.request,
            network['id'],
            port['id'])
        self.assertEqual(ret_val, True)

    def test_quantum_ports_toggle(self):
        network = self.networks['networks'][0]
        port = self.ports['ports'][0]

        quantumclient = self.stub_quantumclient()
        quantumclient.update_port(
            network['id'],
            port['id'],
            {'port': {'state': 'ACTIVE'}}).AndReturn(True)

        self.mox.ReplayAll()

        ret_val = api.quantum_ports_toggle(
            self.request,
            network['id'],
            port['id'],
            'ACTIVE')
        self.assertEqual(ret_val, True)
=======
    def test_network_list(self):
        networks = {'networks': self.api_networks.list()}
        subnets = {'subnets': self.api_subnets.list()}

        quantumclient = self.stub_quantumclient()
        quantumclient.list_networks().AndReturn(networks)
        quantumclient.list_subnets().AndReturn(subnets)
        self.mox.ReplayAll()

        ret_val = api.quantum.network_list(self.request)
        for n in ret_val:
            self.assertIsInstance(n, api.quantum.Network)

    def test_network_get(self):
        network = {'network': self.api_networks.first()}
        subnet = {'subnet': self.api_subnets.first()}
        network_id = self.api_networks.first()['id']
        subnet_id = self.api_networks.first()['subnets'][0]

        quantumclient = self.stub_quantumclient()
        quantumclient.show_network(network_id).AndReturn(network)
        quantumclient.show_subnet(subnet_id).AndReturn(subnet)
        self.mox.ReplayAll()

        ret_val = api.quantum.network_get(self.request, network_id)
        self.assertIsInstance(ret_val, api.quantum.Network)

    def test_network_create(self):
        network = {'network': self.api_networks.first()}

        quantumclient = self.stub_quantumclient()
        form_data = {'network': {'name': 'net1'}}
        quantumclient.create_network(body=form_data).AndReturn(network)
        self.mox.ReplayAll()

        ret_val = api.quantum.network_create(self.request, name='net1')
        self.assertIsInstance(ret_val, api.quantum.Network)

    def test_network_modify(self):
        network = {'network': self.api_networks.first()}
        network_id = self.api_networks.first()['id']

        quantumclient = self.stub_quantumclient()
        form_data = {'network': {'name': 'net1'}}
        quantumclient.update_network(network_id, body=form_data)\
            .AndReturn(network)
        self.mox.ReplayAll()

        ret_val = api.quantum.network_modify(self.request, network_id,
                                             name='net1')
        self.assertIsInstance(ret_val, api.quantum.Network)

    def test_network_delete(self):
        network_id = self.api_networks.first()['id']

        quantumclient = self.stub_quantumclient()
        quantumclient.delete_network(network_id)
        self.mox.ReplayAll()

        api.quantum.network_delete(self.request, network_id)

    def test_subnet_list(self):
        subnets = {'subnets': self.api_subnets.list()}

        quantumclient = self.stub_quantumclient()
        quantumclient.list_subnets().AndReturn(subnets)
        self.mox.ReplayAll()

        ret_val = api.quantum.subnet_list(self.request)
        for n in ret_val:
            self.assertIsInstance(n, api.quantum.Subnet)

    def test_subnet_get(self):
        subnet = {'subnet': self.api_subnets.first()}
        subnet_id = self.api_subnets.first()['id']

        quantumclient = self.stub_quantumclient()
        quantumclient.show_subnet(subnet_id).AndReturn(subnet)
        self.mox.ReplayAll()

        ret_val = api.quantum.subnet_get(self.request, subnet_id)
        self.assertIsInstance(ret_val, api.quantum.Subnet)

    def test_subnet_create(self):
        subnet_data = self.api_subnets.first()
        params = {'network_id': subnet_data['network_id'],
                  'tenant_id': subnet_data['tenant_id'],
                  'name': subnet_data['name'],
                  'cidr': subnet_data['cidr'],
                  'ip_version': subnet_data['ip_version'],
                  'gateway_ip': subnet_data['gateway_ip']}

        quantumclient = self.stub_quantumclient()
        quantumclient.create_subnet(body={'subnet': params})\
            .AndReturn({'subnet': subnet_data})
        self.mox.ReplayAll()

        ret_val = api.quantum.subnet_create(self.request, **params)
        self.assertIsInstance(ret_val, api.quantum.Subnet)

    def test_subnet_modify(self):
        subnet_data = self.api_subnets.first()
        subnet_id = subnet_data['id']
        params = {'name': subnet_data['name'],
                  'gateway_ip': subnet_data['gateway_ip']}

        quantumclient = self.stub_quantumclient()
        quantumclient.update_subnet(subnet_id, body={'subnet': params})\
            .AndReturn({'subnet': subnet_data})
        self.mox.ReplayAll()

        ret_val = api.quantum.subnet_modify(self.request, subnet_id, **params)
        self.assertIsInstance(ret_val, api.quantum.Subnet)

    def test_subnet_delete(self):
        subnet_id = self.api_subnets.first()['id']

        quantumclient = self.stub_quantumclient()
        quantumclient.delete_subnet(subnet_id)
        self.mox.ReplayAll()

        api.quantum.subnet_delete(self.request, subnet_id)

    def test_port_list(self):
        ports = {'ports': self.api_ports.list()}

        quantumclient = self.stub_quantumclient()
        quantumclient.list_ports().AndReturn(ports)
        self.mox.ReplayAll()

        ret_val = api.quantum.port_list(self.request)
        for p in ret_val:
            self.assertIsInstance(p, api.quantum.Port)

    def test_port_get(self):
        port = {'port': self.api_ports.first()}
        port_id = self.api_ports.first()['id']

        quantumclient = self.stub_quantumclient()
        quantumclient.show_port(port_id).AndReturn(port)
        self.mox.ReplayAll()

        ret_val = api.quantum.port_get(self.request, port_id)
        self.assertIsInstance(ret_val, api.quantum.Port)

    def test_port_create(self):
        port_data = self.api_ports.first()
        params = {'network_id': port_data['network_id'],
                  'tenant_id': port_data['tenant_id'],
                  'name': port_data['name'],
                  'device_id': port_data['device_id']}

        quantumclient = self.stub_quantumclient()
        quantumclient.create_port(body={'port': params})\
            .AndReturn({'port': port_data})
        self.mox.ReplayAll()

        ret_val = api.quantum.port_create(self.request, **params)
        self.assertIsInstance(ret_val, api.quantum.Port)
        self.assertEqual(ret_val.id, api.quantum.Port(port_data).id)

    def test_port_modify(self):
        port_data = self.api_ports.first()
        port_id = port_data['id']
        params = {'name': port_data['name'],
                  'device_id': port_data['device_id']}

        quantumclient = self.stub_quantumclient()
        quantumclient.update_port(port_id, body={'port': params})\
            .AndReturn({'port': port_data})
        self.mox.ReplayAll()

        ret_val = api.quantum.port_modify(self.request, port_id, **params)
        self.assertIsInstance(ret_val, api.quantum.Port)
        self.assertEqual(ret_val.id, api.quantum.Port(port_data).id)

    def test_port_delete(self):
        port_id = self.api_ports.first()['id']

        quantumclient = self.stub_quantumclient()
        quantumclient.delete_port(port_id)
        self.mox.ReplayAll()

        api.quantum.port_delete(self.request, port_id)
>>>>>>> master
