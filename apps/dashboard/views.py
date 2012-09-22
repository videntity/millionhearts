#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from ..utils import get_latest_object_or_404
from ..riskassessments.models import ArchimedesRiskAssessment
from django.shortcuts import render_to_response
from django.template import RequestContext

def patient_dashboard(request, patient_id):
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                 patient_id=patient_id)
    
    
    ideal_high=2
    ideal_low=1
    guage_max=1
    guage_min=1
    bmi=20
    height=40
        
    all={ 'wt_numeric': 1,
          'bmi':1, 
          'ideal_high':2,
          'ideal_low':1,
          'guage_max':1,
          'guage_min':1,}
                  
    
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
              
    
    return render_to_response("dashboard/index.html",
                              RequestContext(request,{'patient':patient,
                                'all': all,
                                'latest_wt' : patient.weight,
                                'ideal_low' : ideal_low,
                                'ideal_high' : ideal_high,
                                'guage_min':guage_min,
                                'guage_max': guage_max,
                                'bmi' : bmi,
                                'height' : height}))
