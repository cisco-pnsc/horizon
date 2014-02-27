from django.core.urlresolvers import reverse_lazy

from horizon import forms

from .forms import CreateForm

class CreateView(forms.ModalFormView):
    form_class = CreateForm
    template_name = 'plugins/installers/create.html'
    success_url = reverse_lazy("horizon:plugins:installers:index")