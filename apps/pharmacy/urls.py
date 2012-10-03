#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *


urlpatterns = patterns('',

    url(r'find', find_pharmacy,  name="find_pharmacy"),
    url(r'show', show_pharmacy,  name="show_pharmacy"),
    
    
    url(r'find/(?P<patient_id>\S+)', find_pharmacy,  name="find_pharmacy"),
    url(r'show/(?P<patient_id>\S+)', show_pharmacy,  name="show_pharmacy"),
    
    
    )