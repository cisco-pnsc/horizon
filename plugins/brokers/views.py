from django.core.urlresolvers import reverse_lazy

from horizon import tables
from horizon import forms

from .tables import BrokersTable
from .models import Broker
from .forms import CreateForm

import plugins.api.razor as razor_api
import plugins.api.accessories as accessories

class IndexView(tables.DataTableView):
    table_class = BrokersTable
    template_name = 'plugins/brokers/index.html'
	
    def get_data(self, **kwargs):
	res = []
	for k,v in accessories.convert(razor_api.get_all_brokers()).items():
		server, version = "",""
		if "server" in v["configuration"]:
			server = v["configuration"]["server"]
		if "version" in v["configuration"]:
			version = v["configuration"]["version"]
		res.append(Broker(v["name"],server, version,v["broker-type"]))
	return res

class CreateView(forms.ModalFormView):
    form_class = CreateForm
    template_name = 'plugins/brokers/create.html'
    success_url = reverse_lazy("horizon:plugins:brokers:index")