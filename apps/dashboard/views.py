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
    return render_to_response("dashboard/index.html",
                              RequestContext(request,{}))
