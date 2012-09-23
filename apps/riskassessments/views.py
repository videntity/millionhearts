#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from ..utils import build_pretty_data_view, get_latest_object_or_404
from ..intake.models import PatientProfile
from ..intake import formcopytext
from ..accounts.models import UserProfile
from ..generic.views import generic_form_view, generic_view, generic_view2
from django.db import IntegrityError
from twilio.rest import TwilioRestClient
from django.utils.translation import ugettext_lazy as _

import json
from forms import *
from models import *

def holler_back(request):
    
    # Get these credentials from http://twilio.com/user/account
    client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
    # Make the call
    call = client.calls.create(to="+13046853137", # Any phone number
    from_=settings.TWILIO_DEFAULT_FROM , # Must be a valid Twilio number
    url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")
    print call.sid
    return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(patient.patient_id,)))


def archimedes_hello(request):
    if request.method == 'POST':
        form =  ArchimedesRequiredForm(request.POST)
        
        if form.is_valid():  
            patient = form.save()
            messages.success(request, _("Fantastic. You've taken the step. Your risk assessment is not as accurrate as it could be."))
            messages.success(request, _("Complete blood pressure and cholesterol sections for a more accurate risk assessment."))
            
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(patient.patient_id,)))
                            
        else:
            return render_to_response("generic/bootstrapform.html",
                              RequestContext(request,
                                             {'form': form,}))
    
    
    
    #Just a GET Display and unbound form
    return render_to_response("generic/bootstrapform.html",
                             {'name': "Tell us some basic information",
                              'submit_button_text': "Go On",
                              'form': ArchimedesRequiredForm(),},
                              context_instance = RequestContext(request))





def archimedes_basic_info(request, patient_id):
    
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)

    if request.method == 'POST':
        form =  ArchimedesRequiredForm(request.POST, instance=patient)
        

        if form.is_valid():  
            patient_id = form.save()
            messages.success(request, _("Your basic risk assessment information has been updated."))
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(patient.patient_id,)))
                            
        else:
            messages.error(request, "Oops. The form had errors.")
            return render_to_response("generic/bootstrapform.html",
                              RequestContext(request,
                                             {'form': form,}))
     #Just a GET Display a bound form
    return render_to_response("generic/bootstrapform.html",
                             {'name': "Tell us some basic information",
                              'submit_button_text': "Go On",
                              'form': ArchimedesRequiredForm(instance=patient),},
                              context_instance = RequestContext(request))




def archimedes_blood_pressure(request, patient_id):

    
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)

    if request.method == 'POST':
        form =  ArchimedesBloodPressureForm(request.POST, instance=patient)
        
        if form.is_valid():  
            patient_id = form.save()
            messages.success(request, _("Your blood pressure information has been created/updated."))
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(patient.patient_id,)))

        else:
            return render_to_response("generic/bootstrapform.html",
                              RequestContext(request,
                                             {'form': form,}))
    
    #Just a GET Display a bound form
    return render_to_response("generic/bootstrapform.html",
                             {'name': "Tell us some basic information",
                              'submit_button_text': "Go On",
                              'form': ArchimedesBloodPressureForm(instance=patient),},
                              context_instance = RequestContext(request))




def archimedes_cholesterol(request, patient_id):

    
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)

    if request.method == 'POST':
        form =  ArchimedesCholesterolForm(request.POST, instance=patient)
        
        if form.is_valid():  
            patient_id = form.save()
            messages.success(request, _("Your cholesterol information has been created/updated."))
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(patient.patient_id,)))

        else:            
            return render_to_response("generic/bootstrapform.html",
                              RequestContext(request,
                                             {'form': form,}))
    
    
    #Just a GET Display a bound form
    return render_to_response("generic/bootstrapform.html",
                        {'name': "Tell us some basic information",
                        'submit_button_text': "Go On",
                        'form': ArchimedesCholesterolForm(instance=patient),},
                              context_instance = RequestContext(request))



def archimedes_diabetes(request, patient_id):

    
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)

    if request.method == 'POST':
        form =  ArchimedesDiabetesForm(request.POST, instance=patient)
        
        if form.is_valid():  
            patient_id = form.save()
            messages.success(request, _("Your HbA1c information has been created/updated."))
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(patient.patient_id,)))

        else:            
            return render_to_response("generic/bootstrapform.html",
                              RequestContext(request,
                                             {'form': form,}))
    
    
    #Just a GET Display a bound form
    return render_to_response("generic/bootstrapform.html",
                        {'name': "Tell us some basic information",
                        'submit_button_text': "Go On",
                        'form': ArchimedesDiabetesForm(instance=patient),},
                              context_instance = RequestContext(request))




def archimedes_more(request, patient_id):

    
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)

    if request.method == 'POST':
        form =  ArchimedesMoreForm(request.POST, instance=patient)
        
        if form.is_valid():  
            patient_id = form.save()
            messages.success(request, _("Additonal risk information has been created/updated."))
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(patient.patient_id,)))

        else:
            return render_to_response("generic/bootstrapform.html",
                              RequestContext(request,
                                             {'form': form,}))
    
    
    
    #Just a GET Display and unbound form
    return render_to_response("generic/bootstrapform.html",
                        {'name': "Tell us some basic information",
                        'submit_button_text': "Go On",
                        'form': ArchimedesMoreForm(instance=patient),},
                              context_instance = RequestContext(request))





def archimedes_assessment(request):
    if request.method == 'POST':
        form =  ArchimedesRiskAssessmentForm(request.POST)
        
        if form.is_valid():  
            
            try:
                form.save()
            except(IntegrityError):
                print "here"
                olderArchimedesRiskAssessment.objects.get()
                
                
                
            
            return redirect('patient_dashboard', request.POST['patient_id'])
                            
        else:
            messages.error(request, "Oops. The form had errors.")
            return render_to_response("generic/millionhearts-generic-form.html",
                              RequestContext(request,
                                             {'form': form,}))
    
    
    
    #Just a GET Display and unbound form
    return render_to_response("generic/millionhearts-generic-form.html",
                             {'name': "Take the Risk Assessment",
                              'submit_button_text': "Calclulate Your Risk",
                              'form': ArchimedesRiskAssessmentForm(),
                              'toptext': "toptext",
                              'bottomtext': "bottomtext",},
                              context_instance = RequestContext(request))

def framingahm10yr_assessment(request, pat_id):
    baseform=Framingham10yrHeartRiskTestForm
    basemodel=Framingham10yrHeartRiskTest
    name="Framingham 10 Year Heart Attack Risk Test"
    template="generic/generic-form.html"
    success_redirect='risk-assessments/view/10yrheartrisk-test/' + pat_id

    submit_button_text='Calculate'
    success_message ="Framingham 10 year Risk Assessment Complete."
    
    
    
    
    return generic_form_view(request, pat_id, baseform, basemodel, name,
                             template, success_redirect, submit_button_text,
                             "", "", success_message,
                             form_dict={},
                             formname='Framingham10yrTestForm',
                             create_new_days = settings.FRAMINGHAM10YR_RETEST_DAYS)




def view_framingahm10yr_assessment(request, pat_id):
    name="View 10 Year Framingham Heart Risk Assessment"
    template="generic/pretty-nosigs-view.html"
    
    mo = get_latest_object_or_404(Framingham10yrHeartRiskTest,
                                patient__patient_id=pat_id)
    f=Framingham10yrHeartRiskTestForm(instance=mo)
    data=build_pretty_data_view(form_instance=f, model_object=mo,
                            exclude=(),
                            append=('worker','patient', 'percent_risk'))
    
    #Add some messages
    msg ="The patient's risk for a heart attack in the next 10 years is %s." % (mo.percent_risk)
    messages.success(request,msg)
    
    return render_to_response(template,
                              RequestContext(request,
                                             {'pp':         mo.patient,
                                              'worker':     mo.worker,
                                              'pk':         pat_id,
                                              'data':       data,
                                              'name':       name,
                                              'toptext':    "",
                                              'bottomtext': "",
                                              }))
    
    
    
    
    basemodel=Framingham10yrHeartRiskTest
    name="Framingham10yr Test"
    template="generic/generic-nosigs-view.html"
    signature_url_prefix=""
    return generic_view(request, pat_id, basemodel, name, template,
                        signature_url_prefix,
                        "", "")






def cardio_diabetes_risk_test(request, pat_id):
    baseform=CardioDiabetesRiskTestForm
    basemodel=CardioDiabetesRiskTest
    name="Cardiovascular Disease and Diabetes Risk Assessment"
    template="generic/generic-form.html"
    # success_redirect='client_home'
    success_redirect='/risk-assessments/view/cardio-diabetes-risk-test/'+ pat_id
    submit_button_text='Calculate'
    success_message ="Cardiovascular disease and diabetes risk assessment completed."
    return generic_form_view(request, pat_id, baseform, basemodel, name,
                             template, success_redirect, submit_button_text,
                             "","",
                             success_message,
                             form_dict={},
                             formname='CardioDiabetesRiskTestForm',
                             create_new_days = settings.FRAMINGHAM10YR_RETEST_DAYS)


def cardio_diabetes_risk_test_view(request, pat_id):
    name="View Cardiovascular Disease and Diabetes Risk Assessment"
    template="generic/pretty-nosigs-view.html"
    mo = get_latest_object_or_404(CardioDiabetesRiskTest,
                                patient__patient_id=pat_id)
    f=CardioDiabetesRiskTestForm(instance=mo)
    data=build_pretty_data_view(form_instance=f, model_object=mo,
                            exclude=(),
                            append=('worker','patient'))
    
    #Add some output messages.
    risk_list = json.loads(mo.risk_list)
    for i in risk_list:
        messages.success(request,i)
        
    return render_to_response(template,
                              RequestContext(request,
                                             {'pp':         mo.patient,
                                              'worker':     mo.worker,
                                              'pk':         pat_id,
                                              'data':       data,
                                              'name':       name,
                                              'toptext':    "",
                                              'bottomtext': "",
                                              }))
    
    



def cageaid_screen(request, pat_id):
    baseform=CAGEAIDSubstanceAbuseScreenForm
    basemodel=CAGEAIDSubstanceAbuseScreen
    name="CAGEAID Substance Abuse Screen"
    template="generic/generic-form.html"
    # success_redirect='client_home'
    success_redirect= '/risk-assessments/view/cageaid-screen/' + pat_id
    submit_button_text= 'Calculate'
    success_message ="CAGEAID Substance Abuse Screen completed."
    return generic_form_view(request, pat_id, baseform, basemodel, name,
                             template, success_redirect, submit_button_text,
                             "","",
                             success_message,
                             form_dict={},
                             formname='CAGEAID Substance Abuse Screen',
                             create_new_days = settings.FRAMINGHAM10YR_RETEST_DAYS)




def cageaid_screen_view(request, pat_id):

    template="generic/pretty-nosigs-view.html"
    name="View CAGEAID Substance Abuse Screen"
    mo = get_latest_object_or_404(CAGEAIDSubstanceAbuseScreen,
                                  patient__patient_id=pat_id)
    f=CAGEAIDSubstanceAbuseScreenForm(instance=mo)
    data=build_pretty_data_view(form_instance=f, model_object=mo,
                            exclude=(),
                            append=('worker','patient', 'cage_score',
                                    'recommend_followup'))
    #Add some messages
    if mo.recommend_followup:
        msg ="The patient is recommended for followup concerning his or her potential substance abuse."
        messages.success(request,msg)
    return render_to_response(template,
                              RequestContext(request,
                                             {'pp':         mo.patient,
                                              'worker':     mo.worker,
                                              'pk':         pat_id,
                                              'data':       data,
                                              'name':       name,
                                              'toptext':    "",
                                              'bottomtext': "",
                                              }))
    
@login_required
def ada_type2_screen(request, pat_id):
    baseform=ADAType2DiabetesScreenForm
    basemodel=ADAType2DiabetesScreen
    name="ADA Type-2 Diabetes Screen"
    template="generic/generic-form.html"
    # success_redirect='client_home'
    success_redirect= '/diabetes/view/ada-type2-screen/' + pat_id
    submit_button_text= 'Calculate'
    success_message ="ADA Type-2 Diabetes Screen completed."
    
    
    return generic_form_view(request, pat_id, baseform, basemodel, name,
                             template, success_redirect, submit_button_text,
                             "","",
                             success_message,
                             form_dict={},
                             formname='ADA Type 2 Diabetes Screen',
                             create_new_days = settings.FRAMINGHAM10YR_RETEST_DAYS)



@login_required
def ada_type2_screen_view(request, pat_id):

    template="generic/pretty-nosigs-view.html"
    name="View ADA Type-2 Diabetes Screen"
    mo = get_latest_object_or_404(ADAType2DiabetesScreen,
                                patient__patient_id=pat_id)
   
    f=ADAType2DiabetesScreenForm(instance=mo)
    data=build_pretty_data_view(form_instance=f, model_object=mo,
                            exclude=(),
                            append=('worker','patient', 'risk_score',
                                    'recommend_followup'))
    #Add some messages
    if mo.recommend_followup:
        msg ="The patient is recommended for followup concerning his or her increased risk for Type-2 diabetes."
        messages.success(request,msg)
        
    return render_to_response(template,
                              RequestContext(request,
                                             {'pp':         mo.patient,
                                              'worker':     mo.worker,
                                              'pk':         pat_id,
                                              'data':       data,
                                              'name':       name,
                                              'toptext':    "",
                                              'bottomtext': "",
                                              }))