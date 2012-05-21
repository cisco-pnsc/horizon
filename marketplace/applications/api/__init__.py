import logging
import random

from django.conf import settings

from marketplace.models import *
from horizon import api
from horizon import exceptions

LOG = logging.getLogger(__name__)

def get_all_applications(request, *args, **kwargs):
    return Application.objects.all()

def get_application(request, app_id):
    return Application.objects.get(('id', app_id))

def get_application_flavors(request, app_id):
    return ApplicationInstanceFlavor.objects.filter(('application_id', app_id))

def get_application_versions(request, app_id):
    return ApplicationVersion.objects.filter(('application_id', app_id))

def create_application(request, *args, **kwargs):
    pass

def update_application(request, *args, **kwargs):
    pass

def delete_application(request, *args, **kwargs):
    pass

def create_application_version(request, *args, **kwargs):
    pass

def start_application(request, app_id, flavor, name, version, zone, sec_grp, keypair):
    # Get the glance image associated with this app and version
    app_image = ApplicationVersion.objects.get(('id', version)).image
    # Get application details
    app = get_application(request, app_id)

    server = api.server_create(
        request,
        name,
        app_image,
        flavor,
        keypair,
        False,
        [sec_grp],
        False
    )
    # Stash server and application in the db
    add_application_row(request, app_id, version, server.id)

def add_application_row(request, app_id, version, instance_id):
    row = UserApplication(
            user_id = request.user.id,
            application_id = app_id,
            version = version,
            instance_id = instance_id
          )
    row.save()

def delete_application_row(request, id):
    pass

def stop_application(request, *args, **kwargs):
    pass

def remove_application(request, *args, **kwargs):
    pass
