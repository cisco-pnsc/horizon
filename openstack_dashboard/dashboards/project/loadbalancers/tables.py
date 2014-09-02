# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Copyright 2013, Big Switch Networks, Inc.
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


from django.core.urlresolvers import reverse  # noqa
from django.template import defaultfilters as filters
from django.utils import http
from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import exceptions
from horizon import tables

from openstack_dashboard import api


class AddPoolLink(tables.LinkAction):
    name = "addpool"
    verbose_name = _("Add Pool")
    url = "horizon:project:loadbalancers:addpool"
    classes = ("ajax-modal", "btn-create",)


class AddVipLink(tables.LinkAction):
    name = "addvip"
    verbose_name = _("Add VIP")
    classes = ("ajax-modal", "btn-create",)

    def get_link_url(self, pool):
        base_url = reverse("horizon:project:loadbalancers:addvip",
                           kwargs={'pool_id': pool.id})
        return base_url

    def allowed(self, request, datum=None):
        if datum and datum.vip_id:
            return False
        return True


class AddMemberLink(tables.LinkAction):
    name = "addmember"
    verbose_name = _("Add Member")
    url = "horizon:project:loadbalancers:addmember"
    classes = ("ajax-modal", "btn-create",)


class AddMonitorLink(tables.LinkAction):
    name = "addmonitor"
    verbose_name = _("Add Monitor")
    url = "horizon:project:loadbalancers:addmonitor"
    classes = ("ajax-modal", "btn-create",)

class AddSSLpolicyLink(tables.LinkAction):
    name = "addsslpolicy"
    verbose_name = _("Add SSL Policy")
    url = "horizon:project:loadbalancers:addsslpolicy"
    classes = ("ajax-modal", "btn-create",)
    
class AddSSLcertificateLink(tables.LinkAction):
    name = "addcertificate"
    verbose_name = _("Add SSL Certificate")
    url = "horizon:project:loadbalancers:addcertificate"
    classes = ("ajax-modal", "btn-create",)

class DeleteVipLink(tables.DeleteAction):
    name = "deletevip"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of")
    data_type_singular = _("VIP")
    data_type_plural = _("VIPs")

    def allowed(self, request, datum=None):
        if datum and not datum.vip_id:
            return False
        return True


class DeletePoolLink(tables.DeleteAction):
    name = "deletepool"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of")
    data_type_singular = _("Pool")
    data_type_plural = _("Pools")


class DeleteMonitorLink(tables.DeleteAction):
    name = "deletemonitor"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of")
    data_type_singular = _("Monitor")
    data_type_plural = _("Monitors")


class DeleteSSLpolicyLink(tables.DeleteAction):
    name = "deletesslpolicy"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of")
    data_type_singular = _("SSL Policy")
    data_type_plural = _("SSL Policies")
    
    
class DeleteSSLcertificateLink(tables.DeleteAction):
    name = "deletesslcertificate"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of")
    data_type_singular = _("SSL Certificate")
    data_type_plural = _("SSL Certificates")
    

class DeleteMemberLink(tables.DeleteAction):
    name = "deletemember"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of")
    data_type_singular = _("Member")
    data_type_plural = _("Members")


class UpdatePoolLink(tables.LinkAction):
    name = "updatepool"
    verbose_name = _("Edit Pool")
    classes = ("btn-update",)

    def get_link_url(self, pool):
        base_url = reverse("horizon:project:loadbalancers:updatepool",
                           kwargs={'pool_id': pool.id})
        return base_url


class UpdateVipLink(tables.LinkAction):
    name = "updatevip"
    verbose_name = _("Edit VIP")

    def get_link_url(self, pool):
        base_url = reverse("horizon:project:loadbalancers:updatevip",
                           kwargs={'vip_id': pool.vip_id})
        return base_url

    def allowed(self, request, datum=None):
        if datum and not datum.vip_id:
            return False
        return True


class UpdateMemberLink(tables.LinkAction):
    name = "updatemember"
    verbose_name = _("Edit Member")

    def get_link_url(self, member):
        base_url = reverse("horizon:project:loadbalancers:updatemember",
                           kwargs={'member_id': member.id})
        return base_url


class UpdateMonitorLink(tables.LinkAction):
    name = "updatemonitor"
    verbose_name = _("Edit Monitor")

    def get_link_url(self, monitor):
        base_url = reverse("horizon:project:loadbalancers:updatemonitor",
                           kwargs={'monitor_id': monitor.id})
        return base_url
    
    
class UpdateSSLpolicyLink(tables.LinkAction):
    name = "updatesslpolicy"
    verbose_name = _("Edit SSL Policy")

    def get_link_url(self, sslpolicy):
        base_url = reverse("horizon:project:loadbalancers:updatesslpolicy",
                           kwargs={'sslpolicy_id': sslpolicy.id})
        return base_url
    
class UpdateSSLcertificateLink(tables.LinkAction):
    name = "updatesslcertificate"
    verbose_name = _("Edit SSL Certificate")

    def get_link_url(self, sslcertificate):
        base_url = reverse("horizon:project:loadbalancers:updatesslcertificate",
                           kwargs={'sslcertificate_id': sslcertificate.id})
        return base_url


def get_vip_link(pool):
    if pool.vip_id:
        return reverse("horizon:project:loadbalancers:vipdetails",
                       args=(http.urlquote(pool.vip_id),))
    else:
        return None


class AddPMAssociationLink(tables.LinkAction):
    name = "addassociation"
    verbose_name = _("Add Health Monitor")
    url = "horizon:project:loadbalancers:addassociation"
    classes = ("ajax-modal", "btn-create",)

    def allowed(self, request, datum=None):
        try:
            tenant_id = request.user.tenant_id
            monitors = api.lbaas.pool_health_monitors_get(request,
                                                          tenant_id=tenant_id)
            for m in monitors:
                if m.id not in datum['health_monitors']:
                    return True
        except Exception:
            exceptions.handle(request,
                              _('Failed to retrieve health monitors.'))
        return False


class DeletePMAssociationLink(tables.LinkAction):
    name = "deleteassociation"
    verbose_name = _("Delete Health Monitor")
    url = "horizon:project:loadbalancers:deleteassociation"
    classes = ("ajax-modal", "btn-delete", "btn-danger")

    def allowed(self, request, datum=None):
        if datum and not datum['health_monitors']:
            return False
        return True


class AssociateSSLPolicyLink(tables.LinkAction):
    name = "associatesslpolicy"
    verbose_name = _("Associate SSL Policy")
    classes = ("ajax-modal", "btn-create",)

    def get_link_url(self, pool):
        base_url = reverse("horizon:project:loadbalancers:associatesslpolicy",
                           kwargs={'vip_id': pool.vip_id})
        return base_url

    def allowed(self, request, datum=None):
        if datum and not datum.vip_id:
            return False
        else:
            try:
                vip = api.lbaas.vip_get(request, datum.vip_id)
                if vip['ssl_policy_id'] != None:
                    return False
            except Exception:
                exceptions.handle(request, _('Failed to retrieve VIP'))

        return True


class DisassociateSSLPolicyLink(tables.LinkAction):
    name = "disassociatesslpolicy"
    verbose_name = _("Disassociate SSL Policy")
    classes = ("ajax-modal", "btn-create",)

    def get_link_url(self, pool):
        base_url = reverse("horizon:project:loadbalancers:disassociatesslpolicy",
                           kwargs={'vip_id': pool.vip_id})
        return base_url

    def allowed(self, request, datum=None):
        if datum and datum.vip_id:
            try:
                vip = api.lbaas.vip_get(request, datum.vip_id)
                if vip['ssl_policy_id'] != None:
                    return True

            except Exception:
                exceptions.handle(request, _('Failed to retrieve VIP'))

        return False



class PoolsTable(tables.DataTable):
    name = tables.Column("name",
                       verbose_name=_("Name"),
                       link="horizon:project:loadbalancers:pooldetails")
    description = tables.Column('description', verbose_name=_("Description"))
    provider = tables.Column('provider', verbose_name=_("Provider"),
                             filters=(lambda v: filters.default(v, _('N/A')),))
    subnet_name = tables.Column('subnet_name', verbose_name=_("Subnet"))
    protocol = tables.Column('protocol', verbose_name=_("Protocol"))
    vip_name = tables.Column('vip_name', verbose_name=_("VIP"),
                             link=get_vip_link)

    class Meta:
        name = "poolstable"
        verbose_name = _("Pools")
        table_actions = (AddPoolLink, DeletePoolLink)
        row_actions = (UpdatePoolLink, AddVipLink, UpdateVipLink,
                       DeleteVipLink, AddPMAssociationLink,
                       DeletePMAssociationLink, DeletePoolLink,
                       AssociateSSLPolicyLink, DisassociateSSLPolicyLink)


def get_pool_link(member):
    return reverse("horizon:project:loadbalancers:pooldetails",
                   args=(http.urlquote(member.pool_id),))


def get_member_link(member):
    return reverse("horizon:project:loadbalancers:memberdetails",
                   args=(http.urlquote(member.id),))


class MembersTable(tables.DataTable):
    address = tables.Column('address',
                            verbose_name=_("IP Address"),
                            link=get_member_link,
                            attrs={'data-type': "ip"})
    protocol_port = tables.Column('protocol_port',
                                  verbose_name=_("Protocol Port"))
    pool_name = tables.Column("pool_name",
                            verbose_name=_("Pool"), link=get_pool_link)

    class Meta:
        name = "memberstable"
        verbose_name = _("Members")
        table_actions = (AddMemberLink, DeleteMemberLink)
        row_actions = (UpdateMemberLink, DeleteMemberLink)


class MonitorsTable(tables.DataTable):
    id = tables.Column("id",
                       verbose_name=_("ID"),
                       link="horizon:project:loadbalancers:monitordetails")
    monitorType = tables.Column('type', verbose_name=_("Monitor Type"))

    class Meta:
        name = "monitorstable"
        verbose_name = _("Monitors")
        table_actions = (AddMonitorLink, DeleteMonitorLink)
        row_actions = (UpdateMonitorLink, DeleteMonitorLink)
        
class SSLpoliciesTable(tables.DataTable):
    name = tables.Column("name",
                       verbose_name=_("Name"),
                       link="horizon:project:loadbalancers:sslpolicydetails")
    description = tables.Column('description', verbose_name=_("Description"))
    front_end_enabled = tables.Column('front_end_enabled', verbose_name=_("Front End Enabled"))
    front_end_cipher_suites = tables.Column('front_end_cipher_suites', verbose_name=_("Front End Cipher Suites"))
    front_end_protocols = tables.Column('front_end_protocols', verbose_name=_("Front End Protocols"))
    #back_end_enabled = tables.Column('back_end_enabled', verbose_name=_("Back End Enabled"))
    #back_end_cipher_suites = tables.Column('back_end_cipher_suites', verbose_name=_("Back End Cipher Suites"))
    

    class Meta:
        name = "sslpoliciestable"
        verbose_name = _("SSL Policies")
        table_actions = (AddSSLpolicyLink, DeleteSSLpolicyLink)
        row_actions = (UpdateSSLpolicyLink, DeleteSSLpolicyLink)
        
        
class SSLcertificatesTable(tables.DataTable):
    name = tables.Column("name",
                       verbose_name=_("Name"),
                       link="horizon:project:loadbalancers:sslcertificatedetails")
    #certificate = tables.Column('certificate', verbose_name=_("Certificate"))
    passphrase = tables.Column('passphrase', verbose_name=_("Passphrase"))
    certificate_chain = tables.Column('certificate_chain', verbose_name=_("Certificate Chain"))
    

    class Meta:
        name = "sslcertificatestable"
        verbose_name = _("SSL Certificates")
        table_actions = (AddSSLcertificateLink, DeleteSSLcertificateLink)
        row_actions = (UpdateSSLcertificateLink, DeleteSSLcertificateLink)
