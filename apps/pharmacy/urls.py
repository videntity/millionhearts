#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *


urlpatterns = patterns('',
    
    url(r'find/(?P<patient_id>\S+)', find_pharmacy,  name="find_pharmacy"),
    
    url(r'coupon/(?P<patient_id>\S+)', coupon,  name="coupon"),
    
    
    url(r'find', find_pharmacy,  name="find_pharmacy"),

    url(r'schedule/(?P<origin>[^/]+)/(?P<destination>[^/]+)/(?P<patient_id>\S+)',
                schedule, name="schedule"),


    url(r'directions/(?P<origin>[^/]+)/(?P<destination>\S+)', directions,
                name="directions"),
    
    )