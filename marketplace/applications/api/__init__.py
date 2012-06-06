import Image
import logging
import random
import os
import shutil
import uuid

from django.conf import settings

from marketplace.models import *

from horizon.api.base import APIDictWrapper, url_for
from horizon import api
from horizon import exceptions

LOG = logging.getLogger(__name__)

class App(APIDictWrapper):
    _attrs = ['id','name','instance_id','instance_name','user_id','version',
              'application_id','application_name','uptime']
    
def get_all_applications(request, *args, **kwargs):
    return Application.objects.all()

def get_application(request, app_id):
    return Application.objects.get(('id', app_id))

def get_application_flavors(request, app_id):
    return ApplicationInstanceFlavor.objects.filter(('application_id', app_id))

def get_application_versions(request, app_id):
    return ApplicationVersion.objects.filter(('application_id', app_id))

def get_application_support(request, version_id):
    obj = ApplicationVersion.objects.get(('id',version_id))
    return obj.support

def get_dev_applications(request):
    return Application.objects.filter(('developer', request.user.id))
    
def create_application(request, id, name, description, image,
                       eula, support, icon, base, delivery, 
                       version, flavors, cost, supported, recommended):
    # Store application row
    application = Application(
        id = id,
        name = name,
        description = description,
        eula = eula,
        developer = request.user.id,
        cost = cost,
        icon = icon
    )
    application.save()

    # Resize the icon to 256x256
    img = Image.open(application.icon)
    size = img.size
    img.thumbnail((256, 256), Image.ANTIALIAS)
    # Generate uuid for new image
    img_id = uuid.uuid4()
    ipath = ''.join(("/tmp/",str(img_id)))
    img.save(ipath, "PNG")
    spath = ''.join((settings.APP_MEDIA_ROOT, '/', str(application.icon)))
    os.remove(spath)
    shutil.copy(ipath, spath)
    os.remove(ipath)

    # Store application version
    version = create_application_version(
        request = request,
        application_id = application.id,
        version = version,
        supported = supported,
        support = support,
        image = image
    )

    # Store application flavors
    for flavor in flavors:
        recommend = 0
        if recommended == flavor:
            recommend = 1

        app_flavor = ApplicationInstanceFlavor(
            application_id = application.id,
            flavor_id = flavor,
            recommended = recommend
        )
        app_flavor.save()
    
def update_application(request, *args, **kwargs):
    pass

def delete_application(request, app_id):
    app = Application.objects.get(('id', app_id))
    # Get app icon
    icon = app.icon
    # Delete icon file
    icon.delete()
    app.delete()


def create_application_version(request, application_id, version,
                               image, supported, support):
    version = ApplicationVersion(
        application_id = application_id,
        version = version,
        supported = supported,
        support = support,
        image = image
    )
    version.save()
    return version

def start_application(request, app_id, flavor, name,
                      version, zone, sec_grp, keypair):
    # Get the glance image associated with this app and version
    app_image = ApplicationVersion.objects.get(('id', version)).image
    # Get application details
    app = get_application(request, app_id)
    sec_groups = sec_grp.split(',')
    
    server = api.server_create(
        request,
        name,
        app_image,
        flavor,
        keypair,
        False,
        sec_groups,
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

def delete_user_application(request, id):
    # Get application row
    app = UserApplication.objects.get(('id', id))

    try:
        # Delete server
        api.server_delete(request, app.instance_id)
        # Delete app row
        app.delete()
    except:
        return "Error deleting instance"
    return True

def get_installed_applications(request):
    my_apps = []
    apps = UserApplication.objects.filter(('user_id', request.user.id))
    app_dict = []
    for app in apps:
        app_dict = {
            'id': app.id,
            'application_id': app.application_id,
            'instance_id': app.instance_id,
            'version': app.version
        }
        # Get application name
        application = get_application(request, app.application_id)
        app_dict['application_name'] = application.name
        app_dict['name'] = application.name
        # Get instance name
        instance = api.server_get(request, app.instance_id)
        app_dict['instance_name'] = instance.name
        my_apps.append(App(app_dict))
    return my_apps
