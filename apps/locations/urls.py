#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

    url(r'create$', 'hive.apps.locsetup.views.create', name='loccreate'),
    url(r'select$', 'hive.apps.locsetup.views.select', name='locselect'),
)