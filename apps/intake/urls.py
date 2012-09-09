#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *
urlpatterns = patterns('',

    url(r'^lookup/(?P<pat_id>\S+)$', patient_lookup, name='patent_lookup'),

    url(r'^search-by-name$', search_by_name, name='search_by_name'),

    url(r'^search-by-ssn$', search_by_ssn, name='search_by_ssn'),

    url(r'^create$', initial_intake, name='initial_intake'),
    
    url(r'^quickintake$', quick_intake, name='quick_intake'),
    
    url(r'^quickreferralintake$', quick_referral_intake,
        name='quick_referral_intake'),
    
    url(r'^edit/(?P<pat_id>\S+)$', edit_intake, name='edit_intake'),
    
    url(r'^locator/(?P<pat_id>\S+)$', locator, name='locator'),
    
    url(r'^markvisit/(?P<pat_id>\S+)$', markvisit, name='markvisit'),
    
    url(r'^view-locator/(?P<pat_id>\S+)$', view_locator, name='view_locator'),
    
    )
