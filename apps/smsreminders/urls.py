#!/usr/bin/env python
# -*- coding: utf-8 -*-upons

from django.conf.urls.defaults import patterns, include, url
from views import *
urlpatterns = patterns('',

    url(r'^appointment/search-by-name$', sms_appointment_reminder_search_by_name,
                        name='sms_appointment_reminder_search_by_name'),
    
    url(r'appointment/create/(?P<pat_id>\S+)$', sms_appointment_reminder_create,
                        name='sms_appointment_reminder_create'),

    url(r'^appointment/view/(?P<pk_id>\S+)$', sms_appointment_view,
                        name='sms_appointment_view'),
    
    url(r'adherence/create/(?P<pat_id>\S+)$', sms_adherence_reminder_create,
                        name='sms_adherence_reminder_create'),
    
    url(r'^adherence/search-by-name$', sms_adherence_search_by_name,
                        name='sms_adherence_search_by_name'),

    url(r'^adherence/view/(?P<pk_id>\S+)$', sms_adherence_view,
                        name='sms_adherence_view'),

    url(r'^cron/insert/(?P<cron_key>[^/]+)/$', cron_insert_todays_reminders, name='sms_insert'),
    url(r'^cron/adherence-send/(?P<cron_key>[^/]+)/$', cron_adherence_send, name='cron_adherence_send'),
    url(r'^cron/appointment-send/(?P<cron_key>[^/]+)/$', cron_appointment_send, name='cron_appointment_send'),
    url(r'^cron/adherence-response/(?P<cron_key>[^/]+)/$', cron_process_adherence_responses, name='cron_sms_process_adherence_responses'),    
    
        url(r'^send/$', sms_send, name='sms_send'),
    url(r'^messages/$', sms_messages, name='sms_messages'),
)