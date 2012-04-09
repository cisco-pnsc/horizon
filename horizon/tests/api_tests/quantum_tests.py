# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
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

from quantum.common import exceptions as quantum_exceptions

from horizon import api
from horizon import test


class QuantumApiTests(test.APITestCase):
    def test_get_quantumclient(self):
        """ Verify the client connection method does what we expect. """
        # Replace the original client which is stubbed out in setUp()
        api.quantum.quantumclient = self._original_quantumclient

        client = api.quantum.quantumclient(self.request)
        self.assertEqual(client.auth_tok, self.tokens.first().id)

    def test_quantum_network_list(self):
        network = self.networks.get(id='5d3ad338-4aea-4f97-a4d8-ad9488da9b49')
        quantum_api = self.stub_quantumclient()
        quantum_api.quantum_network_list(self.request)
        
        self.mox.ReplayAll()

        ret_val = api.quantum_network_list(self.request)
        self.assertIsInstance(ret_val, api.quantum.Network)
        self.assertEqual(ret_val._apidict, network)

    def test_quantum_network_create(self):
        pass
    def test_quantum_network_delete(self):
        pass
    def test_quantum_port_list(self):
        pass
    def test_quantum_port_create(self):
        pass
    def test_quantum_port_update(self):
        pass
    def test_quantum_port_attach(self):
        pass
    def test_quantum_port_detach(self):
        pass
    def test_quantum_port_delete(self):
        pass
