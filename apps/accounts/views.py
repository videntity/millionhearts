#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import HttpResponseNotAllowed,  HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.generic.list_detail import object_list
from django.db.models import Sum
from models import *
from forms import SignupForm, LoginForm, SMSCodeForm, PasswordResetRequestForm, PasswordResetForm
from emails import send_reply_email
from django.core.urlresolvers import reverse
from utils import verify
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from models import ValidSMSCode, ValidPasswordResetKey
from datetime import datetime
from django.contrib.auth import logout
from django.contrib import messages

def mylogout(request):
    logout(request)
    return render_to_response('accounts/logout.html',
                              context_instance = RequestContext(request))

    



def reset_password(request, reset_password_key=None):
    try:
        vprk=ValidPasswordResetKey.objects.get(
                                        reset_password_key=reset_password_key)
        
    except:
        return render_to_response('accounts/invalid-key.html',
                              RequestContext(request,
                                             {}))
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            vprk.user.set_password(form.cleaned_data['password1'])
            vprk.user.save()
            vprk.delete()
            logout(request)
            return render_to_response('accounts/reset-password-success.html',
                              RequestContext(request,{}))
        else:
         return render_to_response('accounts/reset-password.html',
                        RequestContext(request, {'form': form,
                            'reset_password_key': reset_password_key}))  
        
    return render_to_response('accounts/reset-password.html',
                              RequestContext(request,
                                    {'form': PasswordResetForm(),
                                    'reset_password_key': reset_password_key}))
        






def password_reset_request(request):
    if request.method == 'POST':

        form = PasswordResetRequestForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            return render_to_response('accounts/password-reset-request.html',
                              RequestContext(request,
                                             {'form': form,
                                              }))
    else:
        return render_to_response('accounts/password-reset-request.html', 
                             {'form': PasswordResetRequestForm()},
                              context_instance = RequestContext(request))
    


def validate_sms(username, smscode):
    try:
        u=User.objects.get(username=username)
        vc=ValidSMSCode.objects.get(user=u, sms_code=smscode)
        now=datetime.now()
    
        if vc.expires < now:
            vc.delete()
            return False
    except(User.DoesNotExist):
        return False        
    except(ValidSMSCode.DoesNotExist):
        return False  
    vc.delete()
    return True


def sms_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            #print "Authenticate"
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']            
            smscode  = form.cleaned_data['smscode']
            if not validate_sms(username=username, smscode=smscode):
                messages.error(request, "Invalid Access Code.")
                return render_to_response('accounts/login.html',
                                          {'form': LoginForm()},
                              RequestContext(request)) 
            
            user=authenticate(username=username, password=password)
            
            if user is not None:

                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    
                    messages.error(request, "Your account is not active.")
                    return HttpResponseRedirect(reverse('sms_code'))
            else:
                messages.error(request, "Invalid username or password.")
                return render_to_response('accounts/login.html',
                                          {'form': LoginForm()},
                              RequestContext(request)) 
        else:
            return render_to_response('accounts/login.html', {'form': form},
                              RequestContext(request))
    return render_to_response('accounts/login.html', {'form': LoginForm()},
                              RequestContext(request)) 

def sms_code(request):
    
    if request.method == 'POST':
        form = SMSCodeForm(request.POST)
        if form.is_valid():
            try:
                u=User.objects.get(username=form.cleaned_data['username'])
                up=u.get_profile()
                if u.is_active:
                    ValidSMSCode.objects.create(user=u)
                    messages.success(request, "A text message was sent to your mobile phone.")
                else:
                    messages.error(request, "Your account is inactive.")
                    return HttpResponseRedirect(reverse('sms_code'))
            except(User.DoesNotExist):
                messages.error(request, "You are not recognized.")
                return HttpResponseRedirect(reverse('sms_code'))
            except(UserProfile.DoesNotExist):
                messages.error(request, "You do not have a user profile.")
                return HttpResponseRedirect(reverse('sms_code'))

            return HttpResponseRedirect(reverse('login'))
        else:
         return render_to_response('accounts/smscode.html',
                              RequestContext(request, {'form': form}))

    return render_to_response('accounts/smscode.html',
                              context_instance = RequestContext(request)) 


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
          new_user = form.save()
          return render_to_response('accounts/signup-complete.html',
                                      RequestContext(request, {}))
        else:
            #return the bound form with errors
            return render_to_response('accounts/signup.html',
                                      RequestContext(request, {'form': form}))      
    else:  
       #this is an HTTP  GET
       return render_to_response('accounts/signup.html',
                                 RequestContext(request,
                                {'form': SignupForm()}))   


def verify_email(request, verification_key,
                 template_name='accounts/activate.html',
                 extra_context=None):
    verification_key = verification_key.lower() # Normalize before trying anything with it.
    account = verify(verification_key)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'account': account},
                              context_instance=context)