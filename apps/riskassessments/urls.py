#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *
urlpatterns = patterns('',

    
    url(r'archimedes$', archimedes_assessment,
        name='archimedes_assessment'),
    
    
    url(r'(?P<pat_id>\S+)$', patient_dashboard,
        name='patient_dashboard'),
    
    
    
    
    url(r'view/cageaid-screen/(?P<pat_id>\S+)$', cageaid_screen_view,
        name='cageaid_screen_view'),    
    url(r'cageaid-screen/(?P<pat_id>\S+)$', cageaid_screen,
        name='cageaid_screen'),
    
    url(r'view/ada-type2-screen/(?P<pat_id>\S+)$', ada_type2_screen_view,
        name='ada_type2_screen_view'),    
    url(r'ada-type2-screen/(?P<pat_id>\S+)$', ada_type2_screen,
        name='ada_type2_screen'),
    
    url(r'view/10yrheartrisk-test/(?P<pat_id>\S+)$', view_framingahm10yr_assessment,
        name='framingahm10yr_assessment_view'),    
    url(r'10yrheartrisk-test/(?P<pat_id>\S+)$', framingahm10yr_assessment,
        name='framingahm10yr_assessment'),

    url(r'view/cardio-diabetes-risk-test/(?P<pat_id>\S+)$',
        cardio_diabetes_risk_test_view,
        name='cardio_diabetes_risk_test_view'),    
    url(r'cardio-diabetes-risk-test/(?P<pat_id>\S+)$', cardio_diabetes_risk_test,
        name='cardio_diabetes_risk_test'),


    

)
