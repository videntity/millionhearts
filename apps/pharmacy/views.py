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
from ..utils import build_pretty_data_view, get_latest_object_or_404
from ..riskassessments.models import ArchimedesRiskAssessment
from ..accounts.models import UserProfile



def coupon(request, patient_id):
    name = _("Coupon")
    
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)
    
    #Just a GET Display a bound form
    return render_to_response("pharmacy/coupon.html",
                             {'name': name,
                              'patient': patient},
                              context_instance = RequestContext(request))
    


def schedule(request, origin, destination, patient_id):
    """ """
    name = _('Please schedule a day to get you blood pressure and cholesterol')
    
    print "SCHEDULE", patient_id
    
    
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)

    if request.method == 'POST':
        form =  ScheduleForm(request.POST, instance = patient)
        
        if form.is_valid():  
            patient_id = form.save()
            messages.success(request, _("Awesome!  Thanks for being heart smart."))
            if UserProfile.objects.filter(patient_id=patient_id) > 0:
                messages.success(request, _("Create an account to get a free follow up via phone or email."))
            
            return HttpResponseRedirect(reverse('coupon',
                                                args=(patient.patient_id,)))
        else:
            
            print form.errors
            return render_to_response("generic/bootstrapform.html",
                              RequestContext(request,
                                             {'form': form,
                                             'name':name }))

    #Just a GET Display a bound form
    return render_to_response("generic/bootstrapform.html",
                             {'name': name,
                              'form': ScheduleForm(instance=patient,
                                                   initial = {
                                                        'origin':origin,
                                                        'destination': destination
                                                        }
                                                   ),},
                              context_instance = RequestContext(request))


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
    return render_to_response("pharmacy/find.html",
                             {'name': _("Find a Participating Pharmacy that Provides Blood Pressure and Cholesterol Screens."),
                              "patient": patient,
                              'form': FindPharmacyForm(),},
                              context_instance = RequestContext(request))