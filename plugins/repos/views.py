from django.core.urlresolvers import reverse_lazy

from horizon import tables
from horizon import forms
from horizon import exceptions

from .tables import ReposTable
from .models import Repo
from .forms import CreateForm

import plugins.api.razor as razor_api
import plugins.api.accessories as accessories

class IndexView(tables.DataTableView):
    table_class = ReposTable
    template_name = 'plugins/repos/index.html'
	
    def get_data(self, **kwargs):
	res = []
	for k,v in accessories.convert(razor_api.get_all_repos()).items():
		res.append(Repo(v["name"],v["iso_url"]))
	return res

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax() and self.request.GET.get("json", False):
            try:
                instances = utils.get_instances_data(self.request)
            except:
                instances = []
                exceptions.handle(request,
                                  _('Unable to retrieve instance list.'))
            data = json.dumps([i._apiresource._info for i in instances])
            return http.HttpResponse(data)
        else:
            return super(IndexView, self).get(request, *args, **kwargs)

class CreateView(forms.ModalFormView):
    form_class = CreateForm
    template_name = 'plugins/repos/create.html'
    success_url = reverse_lazy("horizon:plugins:repos:index")