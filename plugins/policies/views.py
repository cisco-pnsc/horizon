from django.core.urlresolvers import reverse_lazy

from horizon import tables
from horizon import forms
from horizon import exceptions

from .tables import PoliciesTable
from .models import Policy
from .forms import CreateForm

import plugins.api.razor as razor_api
import plugins.api.accessories as accessories

class IndexView(tables.DataTableView):
    table_class = PoliciesTable
    template_name = 'plugins/policies/index.html'
	
    def get_tags_names_as_str(self,tags):
        str = ''
        for tag in tags:
            str += tag['name']
        return str
        
    def get_data(self, **kwargs):
    	res = []
    	for k,v in accessories.convert(razor_api.get_all_policies()).items():
    		res.append(Policy(v["name"],v["repo"]["name"],v["installer"]["name"],v["broker"]["name"],v["configuration"]["hostname_pattern"],v["configuration"]["root_password"],v["max_count"],v["rule_number"],v["tags"],v["enabled"]))
    
        for policy in res:
            policy.tags = self.get_tags_names_as_str(policy.tags)
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
    template_name = 'plugins/policies/create.html'
    success_url = reverse_lazy("horizon:plugins:policies:index")

