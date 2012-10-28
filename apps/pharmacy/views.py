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
import qrencode


def qrcode(request, patient_id):
    
    
    #jr=json.loads("HELLO-WORLD")
    #if jr['status'] != 200:
    #    return json_response
    qrinfo = "https://beheartsmart.com/dashboard/%s" % (patient_i)
    response = HttpResponse(mimetype="image/png")
    image = qrencode.encode_scaled( qrinfo, 400)
    image[2].save(response, "PNG")
    return response

def coupon(request, origin, destination, patient_id):
    name = _("Coupon")
    
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                patient_id=patient_id)
    

    location_list           = patient.destination.split("+")
    location_name = location_list [0]
    destination =""
    for l in location_list[1:]:
        destination="%s+%s" % (destination,l)
    
    print origin, destination
    
    
    
    #Just a GET
    return render_to_response("pharmacy/coupon.html",
                             {"origin": origin,
                              "destination": destination,
                              'location_name': location_name,
                              'name': name,
                              'patient': patient 
                              },
                              context_instance = RequestContext(request))
    
def schedule_no_risk_assessment(request, origin, destination):
    messages.info(request, _("Please complete the risk assessment before scheduling scheduling an appointment."))
    return HttpResponseRedirect(reverse('archimedes_hello',))

def schedule(request, origin, destination, patient_id):
    
    name = _('Schedule a day to get your heart disease screen.')
        
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)

    if request.method == 'POST':
        form =  ScheduleForm(request.POST, instance = patient)
        
        if form.is_valid():  
            patient_id = form.save()
            messages.success(request, _("Awesome!  Thanks for being heart smart."))
            if UserProfile.objects.filter(patient_id=patient_id) > 0:
                messages.success(request, _("Remember to signup for a free reminder."))
            
            return HttpResponseRedirect(reverse('coupon',
                                                args=(origin, destination,
                                                      patient.patient_id,)))
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
    name =  _("Find a Participating Pharmacy that Provides Blood Pressure and Cholesterol Screens.")
    if patient_id:
        patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)
    else:
        patient=None
    
    if request.method == 'POST':
        form =  FindPharmacyForm(request.POST)
        
        if form.is_valid():  
            result = form.save()
            #print result
            #result = json.loads(result)
            if not result['surescripts']['providers']:
                messages.error(request, _("No results were found for you area.  \
                                      This feature is beta and only provides \
                                      results in the state of Ministoa."))
            
            
            
            return render_to_response("pharmacy/show.html",
                              RequestContext(request,
                                             {'result': result,
                                              'patient':patient,
                                              }))   
        else:
            return render_to_response("pharmacy/find.html",
                              RequestContext(request,
                                             {'form': form,
                                              'name':name,
                                              'patient':patient,}))

    
    #Just a GET Display and unbound form
    return render_to_response("pharmacy/find.html",
                             {'name': name,
                              "patient": patient,
                              'form': FindPharmacyForm(),},
                              context_instance = RequestContext(request))