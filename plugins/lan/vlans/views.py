from django.core.urlresolvers import reverse_lazy

from horizon import forms

from .forms import CreateForm,CreateMCPolicyForm

class CreateView(forms.ModalFormView):
    form_class = CreateForm
    template_name = 'plugins/lan/vlans/create.html'
    success_url = reverse_lazy("horizon:plugins:lan:index")
    
class CreateMCPolicyView(forms.ModalFormView):
    form_class = CreateMCPolicyForm
    template_name = 'plugins/lan/vlans/create_mcpolicy.html'
    success_url = reverse_lazy("horizon:plugins:lan:create")
    
    
    