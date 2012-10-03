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
from forms import *
from ..riskassessments.models import ArchimedesRiskAssessment

def show_pharmacy(request, patient_id=None):
    pass


def find_pharmacy(request, patient_id=None):
    
    if patient_id:
        patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)
    else:
        patient=None
    if request.method == 'POST':
        form =  FindPharmacyForm(request.POST)
        
        if form.is_valid():  
            result = form.save()
            
            return render_to_response("pharmacy/show.html",
                              RequestContext(request,
                                             {'result': result,
                                              'patient':patient,
                                              }))   
        else:
            return render_to_response("pharmacy/find.html",
                              RequestContext(request,
                                             {'form': form,
                                              'patient':patient,}))
    
    
    
    #Just a GET Display and unbound form
    return render_to_response("generic/bootstrapform.html",
                             {'name': "Tell us some basic information",
                              'submit_button_text': "Go On",
                              "patient": patient,
                              'form': FindPharmacyForm(),},
                              context_instance = RequestContext(request))