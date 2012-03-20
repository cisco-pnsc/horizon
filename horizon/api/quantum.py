# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Cisco Systems Inc.
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

from __future__ import absolute_import

import functools
import logging
import urlparse

from django.utils.decorators import available_attrs

from quantum.client import Client as quantum_client
from quantum.common import exceptions as quantum_exception

from horizon.api.base import APIDictWrapper, url_for


LOG = logging.getLogger(__name__)


def quantumclient(request):
    o = urlparse.urlparse(url_for(request, 'network'))
    LOG.debug('quantum client connection created for host "%s:%d"' %
                     (o.hostname, o.port))
    return quantum_client(o.hostname,
                          o.port,
                          auth_token=request.user.token)


def network_list(request):
    networks = quantumclient(request).list_networks()
    LOG.debug(networks)


def network_create(request, n_name):
    data = {'network': {'name': n_name}}
    return quantumclient(request).create_network(data)


def network_delete(request, n_uuid):
    quantumclient(request).delete_network(n_uuid)


def network_update(request, *args):
    tenant_id, network_id, param_data, version = args
    data = {'network': {}}
    for kv in param_data.split(","):
        k, v = kv.split("=")
        data['network'][k] = v
    data['network']['id'] = network_id
    
    return quantumclient(request).update_network(network_id, data)


def port_create(request, uuid, num):
    for i in range(num):
        quantumclient(request).create_port(uuid)


def port_delete(request, n_uuid, p_uuid):
    return quantumclient(request).delete_port(n_uuid, p_uuid)


def port_update(request, *args):
    tenant_id, network_id, port_id, param_data, version = args
    data = {'port': {}}
    for kv in param_data.split(","):
        k, v = kv.split("=")
        data['port'][k] = v
    data['network_id'] = network_id
    data['port']['id'] = port_id
    
    return quantumclient(request).update_port(network_id, port_id, data)


def port_attach(request, *args):
    tenant_id, network_id, port_id, attachment, version = args
    data = {'attachment': {'id': '%s' % attachment}}
    
    return quantumclient(request).attach_resource(network_id, port_id, data)


def port_detach(request, *args):
    tenant_id, network_id, port_id, version = args
    
    return quantumclient(request).detach_resource(network_id, port_id)
