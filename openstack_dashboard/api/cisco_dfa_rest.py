# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2013 Cisco Systems, Inc.
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
#
# @author: Nader Lahouti, Cisco Systems, Inc.
#

from __future__ import absolute_import
import logging
import ConfigParser
try:
    import json
except ImportError:
    import simplejson as json
import requests

LOG = logging.getLogger(__name__)

class DFARESTClient(object):
    def __init__(self):
        config_params = read_config_file("/etc/vinci.ini")
        params_dcnm = config_params.get('DCNM')
        params_tenant = config_params.get('Tenant')
        params_os = config_params.get('openstack')
        self._tun_base = params_os.get('dfa_tunnel_base')
        self._ip = params_dcnm.get('ip')
        self._user = params_dcnm.get('user')
        self._pwd = params_dcnm.get('password')
        self._gw_mac = params_tenant.get('gateway_mac')
        if (not self._ip) or (not self._user) or (not self._pwd):
            msg = '[DFARESTClient] Input DCNM IP, user name or password\
                   parameter is not specified'
            raise ValueError, msg
        LOG.debug('[DFARESTClient] DCNM IP: %s, User: %s.'\
                                              % (self._ip, self._user))

        # url timeout: 10 seconds
        self._TIMEOUT_RESPONSE = 10


    def gateway_mac_get(self):
        return self._gw_mac

    def dfa_tun_base_get(self):
        return int(self._tun_base)

    def create_network(self, network_info):
        url = 'http://%s/rest/auto-config/organizations/%s/partitions/%s/networks' \
            % (self._ip, network_info['partitionName'], network_info['partitionName'])
        payload = network_info

        LOG.debug('url = {0}\npayload={1}'.format(url, payload))
        return (self._send_request('POST', url, payload, 'network'))

    def config_profile_get(self, thisprofile):
        url = 'http://%s/rest/auto-config/profiles/%s' \
                                               % (self._ip, thisprofile)
        payload = {}

        LOG.debug('url = {0}'.format(url))
        res = self._send_request('GET', url, payload, 'config-profile')
        return res.json()

    def config_profile_list(self):
        url = 'http://%s/rest/auto-config/profiles' % (self._ip)
        payload = {}

        LOG.debug('url = {0}'.format(url))
        res = self._send_request('GET', url, payload, 'config-profile')
        return res.json()

    def create_org(self, name, desc):
        url = 'http://%s/rest/auto-config/organizations' % (self._ip)
        payload = {
            "organizationName" : name,
            "description" : name if len(desc) == 0 else desc,
            "orchestrationSource" : "OpenStack Controller"
            }

        LOG.debug('create_org: url = {0}'.format(url))
        return (self._send_request('POST', url, payload, 'organization'))

    def create_partition(self, org_name, part_name, desc):
        url = 'http://%s/rest/auto-config/organizations/%s/partitions' \
                          % (self._ip, org_name)
        payload = {
            "partitionName" : part_name,
            "description" : part_name if len(desc) == 0 else desc,
            "organizationName" : org_name
            }

        LOG.debug('create_partition: url = {0}'.format(url))
        return (self._send_request('POST', url, payload, 'partition'))

    def delete_org(self, org_name):
        url = 'http://%s/rest/auto-config/organizations/%s' % \
                                            (self._ip, org_name)
        self._send_request('DELETE', url, '', 'organization')
 
    def delete_partition(self, org_name, partition_name):
        url = 'http://%s/rest/auto-config/organizations/%s/partitions/%s' % \
                                (self._ip, org_name, partition_name)
        self._send_request('DELETE', url, '', 'partition')

    def delete_network(self, network_info):
        org_name = network_info.get('organizationName', '')
        part_name = network_info.get('partitionName', '')
        segment_id = network_info['segmentId']
        url_1 = 'http://%s/rest/auto-config/organizations/' % self._ip
        url_2 = '%s/partitions/%s/networks/segment/%s' % \
                                       (org_name, part_name, segment_id)
        url = url_1 + url_2
        self._send_request('DELETE', url, '', 'network')

    def _login(self):
        url_login = 'http://%s/rest/logon' % (self._ip)
        expiration_time = 100000

        payload = {'expirationTime': expiration_time}
        self._req_headers = {'Accept': 'application/json',
                        'Content-Type': 'application/json; charset=UTF-8'}
        res = requests.post(url_login,
                            data = json.dumps(payload),
                            headers = self._req_headers,
                            auth = (self._user, self._pwd),
                            timeout = self._TIMEOUT_RESPONSE)
        LOG.debug('[DFARESTClient] Login response: %s' % (res.content))
        session_id = ''
        if res and res.status_code >= 200:
            session_id = res.json().get('Dcnm-Token')
        # update global request header  
        self._req_headers.update({'Dcnm-Token': session_id })

    def _logout(self):
        # replace 'sessions' to 'session'
        url_logout = 'http://%s/rest/logout' % (self._ip)
        requests.post(url_logout,
                      headers = self._req_headers,
                      timeout = self._TIMEOUT_RESPONSE)

    def _send_request(self, operation, url, payload, desc):
        res = None
        try:
            payload_json = None
            if payload and payload != '':
                payload_json = json.dumps(payload)
            self._login()
            if operation == 'POST':
                res = requests.post(url,
                                    data = payload_json,
                                    headers = self._req_headers,
                                    timeout = self._TIMEOUT_RESPONSE)
                desc += ' creation'
            elif operation == 'PUT':
                res = requests.put(url,
                                   data = payload_json,
                                   headers = self._req_headers,
                                   timeout = self._TIMEOUT_RESPONSE)
                desc += ' update'
            elif operation == 'DELETE':
                res = requests.delete(url,
                                      data = payload_json,
                                      headers = self._req_headers,
                                      timeout = self._TIMEOUT_RESPONSE)
                desc += ' deletion'
            elif operation == 'GET':
                res = requests.get(url,
                                   data = payload_json,
                                   headers = self._req_headers,
                                   timeout = self._TIMEOUT_RESPONSE)
                desc += ' get'

            LOG.debug('[DFARESTClient] REST Response code: %d, content: %s\n'\
                                        % (res.status_code, res.content))
            if res and res.status_code >= 200:
                LOG.debug('[DFARESTClient] Sent %s to %s successfully.' \
                                     % (desc, url))
            else:
                LOG.debug('[DFARESTClient] Sent %s to %s unsuccessfully.'\
                                                          % (desc, url))

            self._logout()
        except requests.ConnectionError as e:
            # add url to the exception for caller to display
            LOG.debug('Error connecting to {0} '.format(url))
            LOG.exception(str(e))
            raise
        except requests.HTTPError as e:
            LOG.debug('HTTP error')
            LOG.exception(str(e))
            raise
        except requests.Timeout as e:
            LOG.debug('Timeout error')
            LOG.exception(str(e))
            raise

        return res


''' Read initial configuration file'''
def read_config_file(config_file):
    config_params = {}

    parser = ConfigParser.ConfigParser()
    parser.readfp(open(config_file))

    for section in parser.sections():
        section_params = {}
        for option in parser.options(section):
            values = parser.get(section, option)
            if ';' in values:
                values = values.split(';')
            section_params.update({option: values})
        config_params.update({section: section_params})

    return config_params


def check_for_supported_profile(thisprofile):
    '''
    Filter those profiles that are not currently supported.
    '''
    if thisprofile.endswith('Ipv4TfProfile') or \
       thisprofile.endswith('Ipv4EfProfile') or \
       'defaultNetworkL2Profile' in thisprofile:
        return True
    else:
        return False



def get_config_profile_list():
    profile_list = []
    these_profiles = []
    dfa_rest_client = DFARESTClient()
    LOG.debug("dfa_rest_client = {0}".format(dfa_rest_client))
    these_profiles = dfa_rest_client.config_profile_list() 
    LOG.debug("RESULT : {0}".format(these_profiles))
    if len(these_profiles) > 0:
        for i in range(0, len(these_profiles)):
            p = these_profiles[i].get("profileName")
            if check_for_supported_profile(p):
                profile_list.append((p, p))

    return profile_list

def config_profile_list(request, context):
    profile_names = get_config_profile_list()
    return profile_names


def create_org(org_name, description):
    dfa_rest_client = DFARESTClient()
    dfa_rest_client.create_org(org_name, description) 
    return

def create_partition(org_name, part_name, description):
    dfa_rest_client = DFARESTClient()
    dfa_rest_client.create_partition(org_name, part_name, description)
    return


def config_profile_fwding_mode_get(profile_name):
    dfa_rest_client = DFARESTClient()
    profile_params = dfa_rest_client.config_profile_get(profile_name)
    fwd_cli = 'fabric forwarding mode proxy-gateway'
    if fwd_cli in profile_params['configCommands']:
        return 'proxy-gateway'
    else:
        return 'anycast-gateway'

def gateway_mac_get():
    dfa_rest_client = DFARESTClient()
    return dfa_rest_client.gateway_mac_get()

def create_network(tenant_name, network, subnet):
    network_info = {}
    dfa_rest_client = DFARESTClient()
    tun_base = dfa_rest_client.dfa_tun_base_get()
    seg_id = str(network.provider__segmentation_id + tun_base)
    LOG.debug("tenant_id={0} tenant_name={1}\
               segmentation_id={2}".\
               format(network.tenant_id, tenant_name, seg_id))
    subnet_ip_mask = subnet.cidr.split('/')
    gw_ip = subnet.gateway_ip
    cfg_args = []
    cfg_args.append("$segmentId=" + seg_id)
    cfg_args.append("$netMaskLength=" + subnet_ip_mask[1])
    cfg_args.append("$gatewayIpAddress=" + gw_ip)
    cfg_args.append("$networkName=" + network.name)
    cfg_args.append("$vlanId=0")
    cfg_args.append("$vrfName=" + tenant_name + ':' + tenant_name)
    cfg_args = ';'.join(cfg_args)

    ip_range = ""
    for ip_pool in subnet.allocation_pools:
        ip_range += "%s-%s," % (ip_pool['start'], ip_pool['end'])

    dhcp_scopes = {'ipRange': ip_range,
                   'subnet': subnet.cidr,
                   'gateway': gw_ip,
                  }

    network_info = {
          "segmentId" : seg_id,
          "vlanId"    : "0",
          "mobilityDomainId":"None",
          "profileName" : network.config_profile,
          "networkName" : network.name,
          "configArg" : cfg_args,
          "organizationName": tenant_name,
          "partitionName" : tenant_name,
          "description"   : network.name,
          "dhcpScope"     : dhcp_scopes,
    }

    LOG.debug("network_info={0}".format(network_info))

    dfa_rest_client.create_network(network_info)
    return

def delete_network(tenant_name, network):
    network_info = {}
    dfa_rest_client = DFARESTClient()
    tun_base = dfa_rest_client.dfa_tun_base_get()
    seg_id = network.provider__segmentation_id + tun_base
    LOG.debug("tenant_name={0} segmentation_id={1}".format(tenant_name, seg_id))

    network_info = {
        'organizationName': tenant_name,
        'partitionName'   : tenant_name,
        'segmentId'       : seg_id,
    }

    dfa_rest_client.delete_network(network_info)
    return

def delete_tenant(tenant_name):
    dfa_rest_client = DFARESTClient()
    dfa_rest_client.delete_partition(tenant_name, tenant_name)
    dfa_rest_client.delete_org(tenant_name)

