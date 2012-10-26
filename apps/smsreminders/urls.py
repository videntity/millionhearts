#!/usr/bin/env python
# -*- coding: utf-8 -*-upons

from django.conf.urls.defaults import patterns, include, url
from views import *
urlpatterns = patterns('',


    
    url(r'appointment/create/(?P<pat_id>\S+)$', sms_appointment_reminder_create,
                        name='sms_appointment_reminder_create'),

    url(r'^appointment/view/(?P<pk_id>\S+)$', sms_appointment_view,
                        name='sms_appointment_view'),
    

    url(r'^cron/insert/$', cron_insert_todays_reminders, name='sms_insert'),
    url(r'^cron/appointment-send/(?P<cron_key>[^/]+)/$', cron_appointment_send, name='cron_appointment_send'),
       
    url(r'^send/$', sms_send, name='sms_send'),
    url(r'^messages/$', sms_messages, name='sms_messages'),
)