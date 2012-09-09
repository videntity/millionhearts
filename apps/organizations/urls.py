#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *
urlpatterns = patterns('',
    
    url(r'organization/search-by-name$', organization_search_by_name,
        name='organization_search_by_name'),

    url(r'organization/create$', organization_create,
        name='organization_create'),

    url(r'organization/view/(?P<pk>\S+)$', organization_view,
        name='organization_view'),

    url(r'provider/search-by-name$', provider_search_by_name,
        name='organization_search_by_name'),

    url(r'provider/create$', provider_create,
        name='provider_create'),
    
    url(r'provider/view/(?P<pk>\S+)$', provider_view,
        name='provider_view'),
    
    url(r'patient-care-team/create/(?P<pat_id>\S+)$', patient_care_team_create,
        name='patient_care_team_create'),
    
    url(r'patient-care-team/view/(?P<pat_id>\S+)', patient_care_team_view,
        name='patient_care_team_view'),

    url(r'load-providers', load_providers,
        name='load_providers'),

)