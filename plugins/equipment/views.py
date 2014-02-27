import logging

from django import shortcuts
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tabs
from horizon import tables
from horizon import forms
from horizon import exceptions
from horizon import messages

from .forms import AssociateServiceProfileForm,\
                   AssociateMultipleServiceProfilesForm,\
                   ShutdownServerForm,\
                   DisassociateServiceProfileForm,\
                   DownloadDataForm
from .tables import ServersTable
from .models import Server
from .tabs import ServerDetailTabs

import plugins.api.accessories as accessories
import plugins.api.ucs as ucs_api

LOG = logging.getLogger(__name__)

class IndexView(tables.DataTableView):
    table_class = ServersTable
    template_name = 'plugins/equipment/index.html'

    def get_data(self, **kwargs):
        res = []
        for k, v in accessories.convert(ucs_api.get_all_servers()).items():
            res.append(Server(v["id"],v["name"], v["chassis_id"],v["slot_id"], v["cpu"], v["ram"],v["associate"],v["on"], v["fsm"]))
        return res
        
class AssociateServiceProfileView(forms.ModalFormView):
    form_class = AssociateServiceProfileForm
    template_name = 'plugins/equipment/associate.html'
    context_object_name = 'server'
    success_url = reverse_lazy('horizon:plugins:equipment:index')
    failure_url = 'horizon:plugins:equipment:index'

    def get_object(self, *args, **kwargs):
        server_id = self.kwargs['server_id']
        try:
            server = ucs_api.get_server_details(server_id)
            if 'status' in server:
                message =  _('Unable to retrieve details for '
                                'sevrer "%s".') % server_id
                messages.error(self.request,message)
            return server
        except Exception:
            redirect = reverse(self.failure_url)
            msg = _('Unable to retrieve server details.')
            exceptions.handle(self.request, msg, redirect=redirect)
    
    def get_context_data(self, **kwargs):
        context = super(AssociateServiceProfileView, self).get_context_data(**kwargs)
        context['server_id'] = self.kwargs['server_id']
        return context
    
    def get_initial(self):
        server = self.get_object()
       
        return {
                'id' : self.kwargs['server_id'],
              'name': server['name'],
        }  

class DisassociateServiceProfileView(forms.ModalFormView):
    form_class = DisassociateServiceProfileForm
    template_name = 'plugins/equipment/dissociate.html'
    context_object_name = 'server'
    success_url = reverse_lazy('horizon:plugins:equipment:index')
    failure_url = 'horizon:plugins:equipment:index'

    def get_object(self, *args, **kwargs):
        server_id = self.kwargs['server_id']
        try:
            server = ucs_api.get_server_details(server_id)
            
            if 'status' in server:
                message =  _('Unable to retrieve details for '
                                'sevrer "%s".') % server_id
                messages.error(self.request,message)

            if not server['assignedToDn']:
                server['assignedToDn'] = 'Not Assigned'
                server['name'] = 'Unbound'
                
            return {'name' : server['name'], 'profile' : server['assignedToDn']}
        except Exception:
            redirect = reverse(self.failure_url)
            msg = _('Unable to retrieve server details.')
            exceptions.handle(self.request, msg, redirect=redirect)
    
    def get_context_data(self, **kwargs):
        context = super(DisassociateServiceProfileView, self).get_context_data(**kwargs)
        context['server_id'] = self.kwargs['server_id']
        return context
    
    def get_initial(self):
        server = self.get_object()
       
        return {
                'id' : self.kwargs['server_id'],
              'name': server['name'],
              'profile_name' : server['profile']
        }  


                       
class AssociateMultipleServiceProfilesView(forms.ModalFormView):
    form_class = AssociateMultipleServiceProfilesForm
    template_name = 'plugins/equipment/associate_multiple.html'
    context_object_name = 'server'
    success_url = reverse_lazy('horizon:plugins:equipment:index')
    failure_url = 'horizon:plugins:equipment:index'

    def get_context_data(self, **kwargs):
        context = super(AssociateMultipleServiceProfilesView, self).get_context_data(**kwargs)
        return context


class ShutdownServerView(forms.ModalFormView):
    form_class = ShutdownServerForm
    template_name = 'plugins/equipment/shutdown_server.html'
    context_object_name = 'server'
    success_url = reverse_lazy('horizon:plugins:equipment:index')
    failure_url = 'horizon:plugins:equipment:index'

    def get_object(self, *args, **kwargs):
        server_id = self.kwargs['server_id']
        try:
            return {'name' : server_id}
        except Exception:
            redirect = reverse(self.failure_url)
            msg = _('Unable to retrieve tag details.')
            exceptions.handle(self.request, msg, redirect=redirect)
    
    def get_context_data(self, **kwargs):
        context = super(ShutdownServerView, self).get_context_data(**kwargs)
        context['server_id'] = self.kwargs['server_id']
        return context
    
    def get_initial(self):
        server = self.get_object()
       
        return {
                'id' : self.kwargs['server_id'],
              'name': server['name'],
        }
    
def console(request, server_id):
    failure_url = 'horizon:plugins:equipment:index'   
    try:
        kvm_url = ucs_api.get_kvm_url(server_id) 
       
        return shortcuts.redirect(kvm_url)
    except:
        messages.error(request, 'Failed to launch KVM console: %s' % kvm_url)
        return shortcuts.redirect(reverse(failure_url))

class DetailView(tabs.TabView):
    tab_group_class = ServerDetailTabs
    template_name = 'plugins/equipment/detail.html'
    failure_url =  'horizon:plugins:equipment:index'
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context["server"] = self.get_data()
        return context

    def get_data(self):    
      try:
        server_id = self.kwargs['server_id']
        server = ucs_api.get_server_details(server_id)
        
        if 'status' in server:
            message =  _('Unable to retrieve details for '
                                'sevrer "%s".') % server_id
            messages.error(self.request,message)
        return server
      except:
        redirect = reverse(self.failure_url)
        exceptions.handle(self.request,
                              _('Unable to retrieve details for '
                                'sevrer "%s".') % server_id,
                                redirect=redirect)

class DownloadDataView(forms.ModalFormView):
    form_class = DownloadDataForm
    template_name = 'plugins/equipment/download_data_summary.html'
    context_object_name = 'server'
    success_url = reverse_lazy('horizon:plugins:equipment:index')
    failure_url = 'horizon:plugins:equipment:index'

    def get_context_data(self, **kwargs):
        context = super(DownloadDataView, self).get_context_data(**kwargs)
        return context


def download_data(request):
    tenant_id = request.user.tenant_id
    tenant_name = request.user.tenant_name

    template = 'plugins/equipment/data.csv.template'

    try:

        context = {'all_servers_info' : ucs_api.get_context_data(request.session['servers'])}

        response = shortcuts.render(request,
                                    template,
                                    context,
                                    content_type="text/plain")
        
        response['Content-Disposition'] = ('attachment; '
                                           'filename="%s-data.%s"'
                                           % (tenant_name, request.session['format']))
        response['Content-Length'] = str(len(response.content))
        return response

    except Exception as e:
        LOG.exception("Exception in Download Data.csv.")
        messages.error(request, _('Error Downloading Data.csv: %s') % e)
        return shortcuts.redirect(request.build_absolute_uri())

