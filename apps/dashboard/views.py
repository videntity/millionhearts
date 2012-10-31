#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from ..utils import get_latest_object_or_404
from ..riskassessments.models import ArchimedesRiskAssessment
from django.shortcuts import render_to_response
from django.template import RequestContext
from ..accounts.models import UserProfile
from utils import fetch_risks

def calc_progress_percent(patient):
    progress_percent = 0
    if patient.basic_info_complete:
        progress_percent += 20
    if patient.blood_pressure_complete:
        progress_percent += 20
    if patient.cholesterol_complete:
        progress_percent += 20
    if patient.more_complete:
        progress_percent += 20
    
    try:
        up = UserProfile.objects.get(patient_id=patient.patient_id)
        progress_percent += 20
    except(UserProfile.DoesNotExist):
        pass
    
    return progress_percent

def patient_dashboard(request, patient_id):
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                 patient_id=patient_id)
    
    progress_percent = calc_progress_percent(patient)


        
    # height is in inches
    # weight is in pounds (lbs.)
    bmi=(float(patient.weight) * 703) / (float(patient.height) * float(patient.height))
    bmi="%.1f" %(bmi)
    ideal_low= (18.6*float(patient.height) * float(patient.height))/703
    ideal_low="%.1f" % (ideal_low)
    ideal_high=(24.9*float(patient.height) * float(patient.height))/703
    ideal_high="%.1f" % (ideal_high)
    guage_min = float(ideal_low) - 50.0
                        
    if (guage_min < 0):
        guage_min=0.0
                        
    guage_max=float(ideal_high) + 50.0
                    
    if guage_max < float(patient.weight):
        guage_max= float(patient.weight) + 50
        
    if guage_min > float(patient.weight):
        guage_min= float(ideal_low) - 20
              

   
    smoking=0
    if patient.smoker=="yes":
        smoking=1
    
    risks = fetch_risks(patient.archimedes_json_result)
    age_risk = risks['cvdrisk_age']
    
    if risks['ratingForAge']:
        age_risk = risks['ratingForAge']
    
    
    print "risk is ", age_risk  , risks

    
    #if not risks['cvdrisk_upper']['rating']:
    #    absolute_risk = risks['rating']
    #else:
    #    absolute_risk = risks['cvdrisk_age']
    
    
    #risks['cvdrisk_upper']['rating']
    
    
    return render_to_response("dashboard/index.html",
                              RequestContext(request,{'patient':patient,
                                #'absolute_risk': absolute_risk,
                                'age_risk':  float(age_risk),
                                "smoking risk": 1,
                                'weight' : patient.weight,
                                'ideal_low' : ideal_low,
                                'ideal_high' : ideal_high,
                                'guage_min':guage_min,
                                'guage_max': guage_max,
                                'smoking': smoking,
                                'bmi' : float(bmi),
                                'cvdrisk_upper_age': risks['cvdrisk_upper_age'],
                                'cvdrisk_lower_age': risks['cvdrisk_lower_age'],
                                'progress_percent' : calc_progress_percent(patient),
                                'height' : patient.height}))



def recommendations(request, patient_id):
    
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                 patient_id=patient_id)
    
    progress_percent = calc_progress_percent(patient)


        
    # height is in inches
    # weight is in pounds (lbs.)
    bmi=(float(patient.weight) * 703) / (float(patient.height) * float(patient.height))
    bmi="%.1f" %(bmi)
    ideal_low= (18.6*float(patient.height) * float(patient.height))/703
    ideal_low="%.1f" % (ideal_low)
    ideal_high=(24.9*float(patient.height) * float(patient.height))/703
    ideal_high="%.1f" % (ideal_high)
    guage_min = float(ideal_low) - 50.0
                        
    if (guage_min < 0):
        guage_min=0.0
                        
    guage_max=float(ideal_high) + 50.0
                    
    if guage_max < float(patient.weight):
        guage_max= float(patient.weight) + 50
        
    if guage_min > float(patient.weight):
        guage_min= float(ideal_low) - 20
              

    risks = fetch_risks(patient.archimedes_json_result)
    smoking=0
    if patient.smoker=="yes":
        smoking=1
    
   
    
    
    return render_to_response("dashboard/recommendations.html",
                              RequestContext(request,{'patient':patient,
                                "smoking risk": 1,
                                'weight' : patient.weight,
                                'ideal_low' : ideal_low,
                                'ideal_high' : ideal_high,
                                'guage_min':guage_min,
                                'guage_max': guage_max,
                                'smoking': smoking,
                                'bmi' : float(bmi),
                                'progress_percent' : float(calc_progress_percent(patient)),
                                'height' : patient.height}))
    
    
def details(request, patient_id):
    
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                 patient_id=patient_id)
    
    return render_to_response("dashboard/details.html",
                              RequestContext(request,{'patient':patient,
                              }))