# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

SUPPORT_CHOICES = (
    ('S', 'supported'),
    ('L', 'limited_support'),
    ('U', 'unsupported')
)

class Application(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    icon = models.CharField(max_length=255)
    description = models.TextField()
    cost = models.FloatField()
    eula = models.TextField()
    class Meta:
        db_table = u'applications'

class ApplicationInstanceFlavor(models.Model):
    id = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application)
    flavor_id = models.CharField(max_length=255)
    recommended = models.BooleanField(default=False)
    class Meta:
        db_table = u'application_instance_flavors'
        unique_together = (('application', 'flavor_id'),)

class ApplicationVersion(models.Model):
    id = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application)
    version = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    supported = models.CharField(max_length=1, choices=SUPPORT_CHOICES)
    support = models.TextField()
    class Meta:
        db_table = u'application_versions'
        unique_together = (('application', 'version'),)

class UserApplication(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=255)
    application = models.ForeignKey(Application)
    instance_id = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    class Meta:
        db_table = u'user_applications'
