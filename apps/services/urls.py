#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *
urlpatterns = patterns('',
    
    url(r'^search-by-name$', services_search_by_name,
        name='services_search_by_name'),
     
    url(r'referral/browse-past/(?P<pat_id>\S+)$', browse_past_referrals,
        name='services_browse_past_referrals'),
    
    url(r'referral/view/(?P<pk>\S+)$', referral_view,
        name='services_view_referral'),
    
    url(r'referral/create/(?P<pat_id>\S+)$', referral_create,
        name='services_referral_create'),
    
    url(r'linkage/browse-past/(?P<pat_id>\S+)$', browse_past_linkages,
        name='services_browse_past_linkages'),
    
    url(r'linkage/view/(?P<pk>\S+)$', linkage_view,
        name='services_view_linkage'),
    
    #url(r'linkage/create/(?P<pat_id>\S+)$', linkage_create,
    #    name='services_linkage_create'),

    url(r'linkage/select-referral-type/(?P<pat_id>\S+)$', select_referral_type,
        name='select-referral-type'),    

    url(r'linkage/create/(?P<pat_id>\S+)$', linkage_create,
        name='services_linkage_create'), 


    url(r'linkage/follow-up/view/(?P<pk>\S+)$', linkage_followup_view,
        name='services_view_followup_linkage'),
    
    
    url(r'linkage/follow-up/browse/(?P<pk>\S+)$', linkage_followup_browse,
        name='services_browse_followup_linkage'),
    
    url(r'linkage/follow-up/create/(?P<pk>\S+)$', linkage_followup_create,
        name='services_linkage_followup_create'),




    
)
