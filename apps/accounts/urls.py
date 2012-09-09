#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *


urlpatterns = patterns('',

    url(r'login/', sms_login,  name="login"),
    url(r'signup/', signup,  name="account_signup"),
    url(r'smscode/', sms_code, name="sms_code"),
    url(r'logout/', mylogout, name='mylogout'),
    url(r'password-reset-request/', password_reset_request,
        name='password_reset_request'),
    
    url(r'reset-password/(?P<reset_password_key>[^/]+)/$', reset_password,
        name='password_reset_request'),
    
    )