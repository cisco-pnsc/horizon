from django import shortcuts
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon import forms
from horizon import exceptions
from horizon import messages

from .tables import NicsTable 
from .models import Nic
from .forms import AddVlanForm

import plugins.api.ucs as ucs_api
    
class NicsView(tables.DataTableView):
    table_class = NicsTable
    template_name = 'plugins/lan/modify_vlans/modify.html'

    def get_data(self):
        template_id = self.kwargs['template_id']
        try:
            template = ucs_api.get_template_details(template_id)
            self.kwargs['template_name'] = template['name']
            res = []
            for nic in template['nics']:
                res.append(Nic(nic['id'],nic['name']))
            return res
        except Exception:
            redirect = reverse_lazy('plugins:lan:index')
            exceptions.handle(self.request,
                              _('Unable to retrieve profile details.'),
                              redirect=redirect)
        return res

    def get_context_data(self, **kwargs):
        context = super(NicsView, self).get_context_data(**kwargs)
        context["template"] = {'name' : self.kwargs['template_name']}
        context["nics"] = self.get_data()
        return context
    
class AddVlanView(forms.ModalFormView):
    form_class = AddVlanForm
    template_name = 'plugins/lan/modify_vlans/add_vlan.html'
    context_object_name = 'server'
    success_url = reverse_lazy('horizon:plugins:lan:index')
    failure_url = 'horizon:plugins:lan:index'
    
    def get_context_data(self, **kwargs):
        context = super(AddVlanView, self).get_context_data(**kwargs)
        context['nic_id'] = self.kwargs['nic_id']
        return context
    
    def get_initial(self, *args, **kwargs):
        nic_id = self.kwargs['nic_id']
        try:
            nic = ucs_api.get_nic_details(nic_id)
            if 'status' in nic:
                messages.error(self.request,_('Unable to retrieve nic %s details.') % nic_id)
            return nic
        except Exception:
            redirect = reverse(self.failure_url)
            msg = _('Unable to retrieve nic details.')
            exceptions.handle(self.request, msg, redirect=redirect)
        
       