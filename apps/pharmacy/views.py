# Create your views here.
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from ..utils import get_latest_object_or_404
from django.utils.translation import ugettext_lazy as _
from forms import *
from ..riskassessments.models import ArchimedesRiskAssessment



def directions(request, origin=None, destination=None):
    origin = origin.replace("+", " ")
    destination = destination.replace("+", " ")
    #print origin, destination
    return render_to_response("pharmacy/directions.html",
                              RequestContext(request,
                                             {"origin": origin,
                                              "destination": destination}))



def find_pharmacy(request, patient_id=None):
    
    if patient_id:
        patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)
    else:
        patient=None
        print "NO P[ATIENT"
    
    if request.method == 'POST':
        form =  FindPharmacyForm(request.POST)
        
        if form.is_valid():  
            result = form.save()
            #print result
            
            return render_to_response("pharmacy/show.html",
                              RequestContext(request,
                                             {'result': result,
                                              'patient':patient,
                                              }))   
        else:
            return render_to_response("pharmacy/find.html",
                              RequestContext(request,
                                             {'form': form,
                                              'name': _("Find a Participating Pharmacy that Provides Blood Pressure and Cholesterol Screens."),
                                              'patient':patient,}))

    
    #Just a GET Display and unbound form
    return render_to_response("generic/bootstrapform.html",
                             {'name': _("Find a Participating Pharmacy that Provides Blood Pressure and Cholesterol Screens."),
                              "patient": patient,
                              'form': FindPharmacyForm(),},
                              context_instance = RequestContext(request))