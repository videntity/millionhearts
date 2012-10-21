#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

# A collection of handy authentication Backends. Copyright Videntity 2012.
# License: BSD

from django.contrib.auth.models import User
from django.core.validators import email_re
import binascii
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.urlresolvers import get_callable
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import UserProfile


class BasicBackend:
    supports_anonymous_user=False
    supports_object_permissions=False    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class EmailBackend(BasicBackend):
    supports_anonymous_user=False
    supports_object_permissions=False
    def authenticate(self, username=None, password=None):
        #If username is an email address, then try to pull it up
        if email_re.search(username):
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            #We have a non-email address username we should try username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        
        if user.check_password(password):
            return user
        
class MobilePhoneBackend(BasicBackend):
    supports_anonymous_user=False
    supports_object_permissions=False
    def authenticate(self, username=None, password=None):
        try:
            up = UserProfile.objects.get(mobile_phone_number=username)
        except UserProfile.DoesNotExist:
            return None
        
        if up.user.check_password(password):
            return up.user
    
        
class HTTPAuthBackend(BasicBackend):
    supports_anonymous_user=False
    supports_object_permissions=False
    def __init__(self, auth_func=authenticate, realm='API'):
        self.auth_func = auth_func
        self.realm = realm

    def is_authenticated(self, request):
        auth_string = request.META.get('HTTP_AUTHORIZATION', None)
        if not auth_string:
            return False
            
        try:
            (authmeth, auth) = auth_string.split(" ", 1)

            if not authmeth.lower() == 'basic':
                return False

            auth = auth.strip().decode('base64')
            (username, password) = auth.split(':', 1)
        except (ValueError, binascii.Error):
            return False
        
        request.user = self.auth_func(username=username, password=password) \
            or AnonymousUser()
                
        return not request.user in (False, None, AnonymousUser())
        
        
    def authenticate(self, request):
        auth_string = request.META.get('HTTP_AUTHORIZATION', None)

        if not auth_string:
            return AnonymousUser
            
        try:
            (authmeth, auth) = auth_string.split(" ", 1)

            if not authmeth.lower() == 'basic':
                return AnonymousUser

            auth = auth.strip().decode('base64')
            (username, password) = auth.split(':', 1)
        except (ValueError, binascii.Error):
            return AnonymousUser
        
        request.user = self.auth_func(username=username, password=password) \
            or AnonymousUser()
                
        return not request.user in (False, None, AnonymousUser())
        
    def challenge(self):
        resp = HttpResponse("Authorization Required")
        resp['WWW-Authenticate'] = 'Basic realm="%s"' % self.realm
        resp.status_code = 401
        return resp

    def __repr__(self):
        return u'<HTTPBasic: realm=%s>' % self.realm
    



    
    
