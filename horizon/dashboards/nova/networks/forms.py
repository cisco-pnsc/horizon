# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
<<<<<<< HEAD
# Copyright 2012 Cisco Systems Inc.
=======
# Copyright 2012 NEC Corporation
>>>>>>> master
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

import logging

<<<<<<< HEAD
from django import shortcuts
from django.contrib import messages
from django.core import validators
from django.utils.translation import ugettext as _
from novaclient import exceptions as novaclient_exceptions
=======
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
>>>>>>> master

from horizon import api
from horizon import exceptions
from horizon import forms
<<<<<<< HEAD
=======
from horizon import messages
>>>>>>> master


LOG = logging.getLogger(__name__)


<<<<<<< HEAD
class CreateNetwork(forms.SelfHandlingForm):
    name = forms.CharField(max_length=20,
                           label=_("Network Name"),
                           validators=[validators.validate_slug],
                           error_messages={'invalid': _('Network names may '
                                'only contain letters, numbers, underscores '
                                'and hyphens.')})

    def handle(self, request, data):
        try:
            api.quantum_network_create(request, data['name'])
            messages.success(request, _("Network created successfully."))
        except:
            exceptions.handle(request, _('Unable to create network.'))
        return shortcuts.redirect("horizon:nova:networks:index")
=======
class UpdateNetwork(forms.SelfHandlingForm):
    name = forms.CharField(label=_("Name"), required=False)
    tenant_id = forms.CharField(widget=forms.HiddenInput)
    network_id = forms.CharField(label=_("ID"),
                                 widget=forms.TextInput(
                                     attrs={'readonly': 'readonly'}))
    failure_url = 'horizon:nova:networks:index'

    def handle(self, request, data):
        try:
            network = api.quantum.network_modify(request, data['network_id'],
                                         name=data['name'])
            msg = _('Network %s was successfully updated.') % data['name']
            LOG.debug(msg)
            messages.success(request, msg)
            return network
        except:
            msg = _('Failed to update network %s') % data['name']
            LOG.info(msg)
            redirect = reverse(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)
>>>>>>> master
