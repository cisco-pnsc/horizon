from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from plugins.lan.modify_vlans import views as views

VIEW_MOD = 'plugins.lan.modify_vlans.views'


urlpatterns = patterns(VIEW_MOD,
   url(r'^(?P<template_id>[^/]+)/$', views.NicsView.as_view(),name='modify'),
   url(r'^(?P<nic_id>[^/]+)/add$', views.AddVlanView.as_view(), name='add'),
    
)
