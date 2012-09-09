#!/usr/bin/env python
# -*- coding: utf-8 -*-upons

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

    url(r'issue-coupons/(?P<pat_id>\S+)$',
            'hive.apps.coupons.views.issue_coupons',
            name=' issue_coupons'),
    
    url(r'^search-by-name$', 'hive.apps.coupons.views.search_by_name',
        name='coupons_search_by_name'),
    
)