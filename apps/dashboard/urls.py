#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *
urlpatterns = patterns('',

    
    url(r'(?P<patient_id>\S+)$', patient_dashboard,
        name='patient_dashboard'), 

)
