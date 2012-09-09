#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from forms import LocationSetupForm
from models import LocationSetup
from django.core.urlresolvers import reverse
from ..accounts.models import UserProfile

# Create your views here.

@login_required
def create(request):
    if request.method == 'POST':

        form = LocationSetupForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            loc=form.save()
            
            up=request.user.get_profile()
            
            up.location=loc
            up.save()
            
            return HttpResponseRedirect(reverse('home'))            
        else:
            message="Form Error."
            locations=LocationSetup.objects.all()
            return render_to_response('locsetup/locsetup.html',
                              RequestContext(request,
                                             {'form': form,
                                              'updated' : message,
                                              'locations': locations
                                              }))
    else:
        locations=LocationSetup.objects.all()
        
        
        return render_to_response('locsetup/locsetup.html', 
                             {'form': LocationSetupForm(), 'locations': locations},
                              context_instance = RequestContext(request))



@login_required
def select(request):
    if request.method == 'POST' and request.POST.has_key('locations'):
        up=request.user.get_profile()
        location=LocationSetup.objects.get(pk=request.POST['locations'])
        up.location=location
        up.save()
        return HttpResponseRedirect(reverse('home'))            
    return HttpResponseRedirect(reverse('loccreate'))