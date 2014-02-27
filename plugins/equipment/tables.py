import logging

from horizon import messages
from horizon import tables
from horizon import exceptions

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .models import Server

import plugins.api.ucs as ucs_api

LOG = logging.getLogger(__name__)

class ServerFilterAction(tables.FilterAction):

    def filter(self, table, servers, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()
        return [server for server in servers
                if q in server.name.lower()]

class AssociateServiceProfile(tables.LinkAction):
    name = "associate_service_profile"
    verbose_name = _("Associate Service Profile")
    url = "horizon:plugins:equipment:associate"
    classes = ("ajax-modal", "btn-associate")

    def allowed(self, request, server=None):
        try:
            if server is not None:
                return server.associate == False
            return False
        except:
            return False

class AssociateMultipleServiceProfiles(tables.LinkAction):
    name = "associate_multiple"
    verbose_name = _("Associate Service Profile to Multiple Servers")
    url  = "horizon:plugins:equipment:associate_multiple"
    classes = ("ajax-modal", "btn-associate_multiple")


class DissociateServiceProfile(tables.LinkAction):
    name = "disassociate_service_profile"
    verbose_name = _("Dissociate Service Profile")
    url = "horizon:plugins:equipment:dissociate"
    classes = ("btn-danger","ajax-modal", "btn-dissociate")

    def allowed(self, request, server=None):
        try:
            if server is not None:
                return server.associate == True
            return False
        except:
            return False
            
class BootServer(tables.BatchAction):
    ajax = True
    name = "boot_server"
    data_type_singular = _("Server")
    classes = ('btn-danger', 'btn-boot')
    action_present = _("Boot")
    action_past = _("Boot")

    def allowed(self, request, server=None):
        try:
            if server is not None:
                return server.associate == True and server.on == 'off'
            return False
        except:
            return False
            
    def action(self, request, obj_id):
        ucs_api.boot_server(obj_id)
        
class ShutdownServer(tables.LinkAction):
    name = "shutdown"
    verbose_name = _("Shutdown Server")
    url = "horizon:plugins:equipment:shutdown"
    classes = ("ajax-modal", "btn-danger", "btn-shutdown")

    def allowed(self, request, server=None):
        try:
            if server is not None:
                return server.associate == True and server.on == 'on'
            return False
        except:
            return False


class KVMConsole(tables.LinkAction):
    name = "kvm_console"
    verbose_name = _("KVM Console")
    url  = "horizon:plugins:equipment:console"
    classes = ("btn-kvmconsole")

class ResetServer(tables.BatchAction):
    ajax = True
    name = "Reset_server"
    data_type_singular = _("Server")
    classes = ('btn-danger', 'btn-Reset')
    action_present = _("Reset")
    action_past = _("Reset")
            
    def action(self, request, obj_id):
        ucs_api.reset_server(obj_id)   
  
class UpdateRow(tables.Row):
    ajax = True
    failure_url = "horizon:plugins:equipment:index"

    def get_data(self, request, server_id):
        server = ucs_api.get_server_details(server_id)
        try:
            if 'status' in server:
                messages.error(request, server['errorDescr'])
                return Server(server_id,server_id,'','','','',False,'',100)
            return Server(server['id'],server['name'],server['chassis_id'],server['slot_id'],server['cpu'],server['ram'],server['associate'],server['on'], server['fsm'])
        except Exception:
            msg = _('Failed to retrieve server details.') 
            LOG.info(msg)
            redirect = reverse(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)
            

class DownloadData(tables.LinkAction):
    name = "download_data"
    verbose_name = _("Download Summary")
    verbose_name_plural = _("Download Summary")
    classes = ("btn-download","ajax-modal")
    url = "horizon:plugins:equipment:download"

class ServersTable(tables.DataTable):
    
    STATUS_CHOICES = (
        ('100%', True),
        ('None', True)
    )

    name = tables.Column('name', verbose_name=_("Name"),link='horizon:plugins:equipment:detail')
    chassis = tables.Column('chassis', verbose_name=_("Chassis"))
    slot = tables.Column('slot', verbose_name=_("Slot"))
    cpu = tables.Column('cpu', verbose_name=_("CPUs"))
    ram = tables.Column('ram', verbose_name=_("RAM"))
    associate = tables.Column('associate', verbose_name=_("Associate"))
    power_state = tables.Column('on', verbose_name=_("Power State"))
    state = tables.Column('state', verbose_name=_("Percent Progress"),status=True,
                status_choices=STATUS_CHOICES)

  
    class Meta:
        name = "servers"
        verbose_name = _("Servers")
        table_actions = (AssociateMultipleServiceProfiles,DownloadData,ServerFilterAction,)
        row_actions = (AssociateServiceProfile,DissociateServiceProfile,ResetServer,BootServer,ShutdownServer,KVMConsole)
        status_columns = ["state"]
        row_class = UpdateRow
        multi_select = True
