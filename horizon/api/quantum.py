# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
<<<<<<< HEAD
# Copyright 2012 Cisco Systems Inc.
=======
# Copyright 2012 Cisco Systems, Inc.
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

from __future__ import absolute_import

<<<<<<< HEAD
import functools
import logging
import urlparse

from django.utils.decorators import available_attrs

import quantumclient as quantum_client
from quantumclient.common import exceptions as quantum_exception

from horizon.api.base import APIDictWrapper, url_for
from horizon.api import nova
=======
import logging

from quantumclient.v2_0 import client as quantum_client
from django.utils.datastructures import SortedDict

from horizon.api.base import APIDictWrapper, url_for

>>>>>>> master

LOG = logging.getLogger(__name__)


<<<<<<< HEAD
class Network(APIDictWrapper):
    _attrs = ['id', 'name', 'port_count']


class Port(APIDictWrapper):
    _attrs = ['id', 'attachment_server', 'attachment_id', 'state', 'op-status']


class Vif(APIDictWrapper):
    _attrs = ['id']


def quantumclient(request):
    o = urlparse.urlparse(url_for(request, 'network'))
    LOG.debug('quantum client connection created for host "%s:%d"' %
              (o.hostname, o.port))
    return quantum_client.Client(o.hostname,
                                 o.port,
                                 tenant=request.user.tenant_id,
                                 auth_token=request.user.token)


def quantum_network_list(request):
    q_networks = quantumclient(request).list_networks()
    networks = []
    for network in q_networks['networks']:
        # Get detail for this network
        det = quantumclient(request).show_network_details(network['id'])
        # Get ports for this network
        ports = quantumclient(request).list_ports(network['id'])
        det['network']['port_count'] = len(ports['ports'])
        networks.append(Network(det['network']))
    return networks


def quantum_network_create(request, n_name):
    data = {'network': {'name': n_name}}
    return quantumclient(request).create_network(data)


def quantum_network_delete(request, n_uuid):
    return quantumclient(request).delete_network(n_uuid)


def quantum_network_update(request, *args):
    tenant_id, network_id, param_data, version = args
    data = {'network': {}}
    for kv in param_data.split(","):
        k, v = kv.split("=")
        data['network'][k] = v
    data['network']['id'] = network_id

    return quantumclient(request).update_network(network_id, data)


def quantum_network_details(request, n_uuid):
    details = quantumclient(request).show_network_details(n_uuid)
    return details


def quantum_port_list(request, n_uuid):
    q_ports = quantumclient(request).list_ports(n_uuid)
    ports = []
    for port in q_ports['ports']:
        # Get port details
        det = quantumclient(request).show_port_details(n_uuid, port['id'])
        att = quantumclient(request).show_port_attachment(n_uuid, port['id'])
        # Get server name from id
        if 'id' in att['attachment']:
            server = get_interface_server(request, att['attachment']['id'])
            det['port']['attachment_server'] = server.name
            det['port']['attachment_id'] = att['attachment']['id']
        else:
            det['port']['attachment_id'] = None
            det['port']['attachment_server'] = None
        ports.append(Port(det['port']))
    return ports


def quantum_port_create(request, num, uuid):
    for i in range(int(num)):
        quantumclient(request).create_port(uuid)


def quantum_port_delete(request, n_uuid, p_uuid):
    return quantumclient(request).delete_port(n_uuid, p_uuid)


def quantum_port_update(request, *args):
    tenant_id, network_id, port_id, param_data, version = args
    data = {'port': {}}
    for kv in param_data.split(","):
        k, v = kv.split("=")
        data['port'][k] = v
    data['network_id'] = network_id
    data['port']['id'] = port_id

    return quantumclient(request).update_port(network_id, port_id, data)


def quantum_port_attach(request, network_id, port_id, attachment):
    data = {'attachment': {'id': '%s' % attachment}}

    return quantumclient(request).attach_resource(network_id, port_id, data)


def quantum_port_detach(request, network_id, port_id):
    return quantumclient(request).detach_resource(network_id, port_id)


def quantum_ports_toggle(request, network_id, port_id, state):
    data = {'port': {'state': state}}
    return quantumclient(request).update_port(network_id, port_id, data)


def get_free_interfaces(request):
    instance_interfaces = []
    attached_interfaces = []
    # Fetch a list of networks
    networks = quantum_network_list(request)
    for network in networks:
        # Get all ports
        ports = quantum_port_list(request, network.id)
        for port in ports:
            # Check for attachments
            if port.attachment_id:
                attached_interfaces.append(port.attachment_id)

    # Get all instances
    instances = nova.server_list(request)
    for instance in instances:
        vifs = nova.virtual_interfaces_list(request, instance.id)
        for vif in vifs:
            if not any(vif.id in s for s in attached_interfaces):
                instance_interfaces.append(
                {'instance': instance.name, 'vif': vif.id})
    return instance_interfaces


def get_interface_server(request, interface):
    # Get all instances
    instances = nova.server_list(request)
    for instance in instances:
        vifs = nova.virtual_interfaces_list(request, instance.id)
        for vif in vifs:
            if vif.id == interface:
                return instance
    return None
=======
class QuantumAPIDictWrapper(APIDictWrapper):

    def set_id_as_name_if_empty(self, length=8):
        try:
            if not self._apidict['name']:
                id = self._apidict['id']
                if length:
                    id = id[:length]
                self._apidict['name'] = '(%s)' % id
        except KeyError:
            pass

    def items(self):
        return self._apidict.items()


class Network(QuantumAPIDictWrapper):
    """Wrapper for quantum Networks"""
    _attrs = ['name', 'id', 'subnets', 'tenant_id', 'status', 'admin_state_up']

    def __init__(self, apiresource):
        apiresource['admin_state'] = \
            'UP' if apiresource['admin_state_up'] else 'DOWN'
        super(Network, self).__init__(apiresource)


class Subnet(QuantumAPIDictWrapper):
    """Wrapper for quantum subnets"""
    _attrs = ['name', 'id', 'cidr', 'network_id', 'tenant_id',
              'ip_version', 'ipver_str']

    def __init__(self, apiresource):
        apiresource['ipver_str'] = get_ipver_str(apiresource['ip_version'])
        super(Subnet, self).__init__(apiresource)


class Port(QuantumAPIDictWrapper):
    """Wrapper for quantum ports"""
    _attrs = ['name', 'id', 'network_id', 'tenant_id',
              'admin_state_up', 'status', 'mac_address',
              'fixed_ips', 'host_routes', 'device_id']

    def __init__(self, apiresource):
        apiresource['admin_state'] = \
            'UP' if apiresource['admin_state_up'] else 'DOWN'
        super(Port, self).__init__(apiresource)


IP_VERSION_DICT = {4: 'IPv4', 6: 'IPv6'}


def get_ipver_str(ip_version):
    """Convert an ip version number to a human-friendly string"""
    return IP_VERSION_DICT.get(ip_version, '')


def quantumclient(request):
    LOG.debug('quantumclient connection created using token "%s" and url "%s"'
              % (request.user.token.id, url_for(request, 'network')))
    LOG.debug('user_id=%(user)s, tenant_id=%(tenant)s' %
              {'user': request.user.id, 'tenant': request.user.tenant_id})
    c = quantum_client.Client(token=request.user.token.id,
                              endpoint_url=url_for(request, 'network'))
    return c


def network_list(request, **params):
    LOG.debug("network_list(): params=%s" % (params))
    networks = quantumclient(request).list_networks(**params).get('networks')
    # Get subnet list to expand subnet info in network list.
    subnets = subnet_list(request)
    subnet_dict = SortedDict([(s['id'], s) for s in subnets])
    # Expand subnet list from subnet_id to values.
    for n in networks:
        n['subnets'] = [subnet_dict[s] for s in n['subnets']]
    return [Network(n) for n in networks]


def network_get(request, network_id, **params):
    LOG.debug("network_get(): netid=%s, params=%s" % (network_id, params))
    network = quantumclient(request).show_network(network_id,
                                                  **params).get('network')
    # Since the number of subnets per network must be small,
    # call subnet_get() for each subnet instead of calling
    # subnet_list() once.
    network['subnets'] = [subnet_get(request, sid)
                          for sid in network['subnets']]
    return Network(network)


def network_create(request, **kwargs):
    """
    Create a subnet on a specified network.
    :param request: request context
    :param tenant_id: (optional) tenant id of the network created
    :param name: (optional) name of the network created
    :returns: Subnet object
    """
    LOG.debug("network_create(): kwargs = %s" % kwargs)
    body = {'network': kwargs}
    network = quantumclient(request).create_network(body=body).get('network')
    return Network(network)


def network_modify(request, network_id, **kwargs):
    LOG.debug("network_modify(): netid=%s, params=%s" % (network_id, kwargs))
    body = {'network': kwargs}
    network = quantumclient(request).update_network(network_id,
                                                    body=body).get('network')
    return Network(network)


def network_delete(request, network_id):
    LOG.debug("network_delete(): netid=%s" % network_id)
    quantumclient(request).delete_network(network_id)


def subnet_list(request, **params):
    LOG.debug("subnet_list(): params=%s" % (params))
    subnets = quantumclient(request).list_subnets(**params).get('subnets')
    return [Subnet(s) for s in subnets]


def subnet_get(request, subnet_id, **params):
    LOG.debug("subnet_get(): subnetid=%s, params=%s" % (subnet_id, params))
    subnet = quantumclient(request).show_subnet(subnet_id,
                                                **params).get('subnet')
    return Subnet(subnet)


def subnet_create(request, network_id, cidr, ip_version, **kwargs):
    """
    Create a subnet on a specified network.
    :param request: request context
    :param network_id: network id a subnet is created on
    :param cidr: subnet IP address range
    :param ip_version: IP version (4 or 6)
    :param gateway_ip: (optional) IP address of gateway
    :param tenant_id: (optional) tenant id of the subnet created
    :param name: (optional) name of the subnet created
    :returns: Subnet object
    """
    LOG.debug("subnet_create(): netid=%s, cidr=%s, ipver=%d, kwargs=%s"
              % (network_id, cidr, ip_version, kwargs))
    body = {'subnet':
                {'network_id': network_id,
                 'ip_version': ip_version,
                 'cidr': cidr}}
    body['subnet'].update(kwargs)
    subnet = quantumclient(request).create_subnet(body=body).get('subnet')
    return Subnet(subnet)


def subnet_modify(request, subnet_id, **kwargs):
    LOG.debug("subnet_modify(): subnetid=%s, kwargs=%s" % (subnet_id, kwargs))
    body = {'subnet': kwargs}
    subnet = quantumclient(request).update_subnet(subnet_id,
                                                  body=body).get('subnet')
    return Subnet(subnet)


def subnet_delete(request, subnet_id):
    LOG.debug("subnet_delete(): subnetid=%s" % subnet_id)
    quantumclient(request).delete_subnet(subnet_id)


def port_list(request, **params):
    LOG.debug("port_list(): params=%s" % (params))
    ports = quantumclient(request).list_ports(**params).get('ports')
    return [Port(p) for p in ports]


def port_get(request, port_id, **params):
    LOG.debug("port_get(): portid=%s, params=%s" % (port_id, params))
    port = quantumclient(request).show_port(port_id, **params).get('port')
    return Port(port)


def port_create(request, network_id, **kwargs):
    """
    Create a port on a specified network.
    :param request: request context
    :param network_id: network id a subnet is created on
    :param device_id: (optional) device id attached to the port
    :param tenant_id: (optional) tenant id of the port created
    :param name: (optional) name of the port created
    :returns: Port object
    """
    LOG.debug("port_create(): netid=%s, kwargs=%s" % (network_id, kwargs))
    body = {'port': {'network_id': network_id}}
    body['port'].update(kwargs)
    port = quantumclient(request).create_port(body=body).get('port')
    return Port(port)


def port_delete(request, port_id):
    LOG.debug("port_delete(): portid=%s" % port_id)
    quantumclient(request).delete_port(port_id)


def port_modify(request, port_id, **kwargs):
    LOG.debug("port_modify(): portid=%s, kwargs=%s" % (port_id, kwargs))
    body = {'port': kwargs}
    port = quantumclient(request).update_port(port_id, body=body).get('port')
    return Port(port)
>>>>>>> master
