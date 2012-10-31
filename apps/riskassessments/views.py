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
from utils import send_sms_twilio
from django.core.mail import send_mail
import json
from forms import *
from models import *

def tomorrow():
    return datetime.date.today() + timedelta(days=1)

def holler_back(request):    
    
    t = tomorrow()
    # Get these credentials from http://twilio.com/user/account
    reminders_to_send = ArchimedesRiskAssessment.objects.filter(followup_date = t,
                                                                follow_up_complete=False)
    for i in reminders_to_send:
        print i.patient_id
        try:
            up = UserProfile.objects.get(patient_id=i.patient_id)
            
            #send a text message
            if up.preferred_contact_method == "sms" and \
               up.mobile_phone_number:
                send_sms_twilio(settings.SMS_REMINDER_MESSAGE,
                                up.mobile_phone_number)
                i.follow_up_complete = True
                i.save()
            
            #send an email if they prefer
            if up.preferred_contact_method == "email" and \
               up.user.email:
                msg = """
                %s
                
                %s/pharmacy/coupon/%s/%s/%s
                """ % (settings.EMAIL_REMINDER_BODY, settings.HOSTNAME_URL,
                       i.origin,  i.destination, i.patient_id)
                
                send_mail(settings.EMAIL_REMINDER_SUBJECT , msg,
                          settings.DEFAULT_FROM_EMAIL,
                          [up.user.email,], fail_silently=False)
                
                
                send_sms_twilio(settings.SMS_REMINDER_MESSAGE,
                                up.mobile_phone_number)
                i.follow_up_complete = True
                i.save()
                
            
            
        except(UserProfile.DoesNotExist):
            pass
            
    
        #send_sms_twilio("hello", "+13046853137")
    
    
    #client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
    # Make the call
    #call = client.calls.create(to="+13046853137", # Any phone number
    #from_=settings.TWILIO_DEFAULT_FROM , # Must be a valid Twilio number
    #url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")
    #print call.sid
    return HttpResponse("OK")




def archimedes_schedule(request, patient_id):
    """ """
    name = _('Please schedule a day to get you blood pressure and cholesterol')
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)

    if request.method == 'POST':
        form =  ArchimedesScheduleForm(request.POST, instance=patient)
        
        if form.is_valid():  
            patient_id = form.save()
            messages.success(request, _("Awesome!  Thanks for being heart smart."))
            if UserProfile.objects.filter(patient_id=patient_id) > 0:
                messages.success(request, _("Create an account to get a free follow up to your phone or email."))
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(patient.patient_id,)))
        else:
            return render_to_response("generic/bootstrapform.html",
                              RequestContext(request,
                                             {'form': form,
                                             'name':name }))
    
    #Just a GET Display a bound form
    return render_to_response("generic/bootstrapform.html",
                             {'name': name,
                              'form': ArchimedesFollowUpForm(instance=patient),},
                              context_instance = RequestContext(request))




def archimedes_followup(request, patient_id):
    """ """
    name = _('Please schedule a day to get you blood pressure and cholesterol')
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)

    if request.method == 'POST':
        form =  ArchimedesFollowUpForm(request.POST, instance=patient)
        
        if form.is_valid():  
            patient_id = form.save()
            messages.success(request, _("Awesome!  Thanks for being heart smart."))
            if UserProfile.objects.filter(patient_id=patient_id) > 0:
                messages.success(request, _("Create an account to get a free follow up to your phone or email."))
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(patient.patient_id,)))
        else:
            return render_to_response("generic/bootstrapform.html",
                              RequestContext(request,
                                             {'form': form,
                                             'name':name }))
    
    #Just a GET Display a bound form
    return render_to_response("generic/bootstrapform.html",
                             {'name': name,
                              'form': ArchimedesFollowUpForm(instance=patient),},
                              context_instance = RequestContext(request))





def archimedes_hello(request):
    if request.method == 'POST':
        form =  ArchimedesRequiredForm(request.POST)
        
        if form.is_valid():  
            patient = form.save(commit = False)
            patient.client_ip         = request.META.get('REMOTE_ADDR')
            patient.language_code     = request.LANGUAGE_CODE
            patient.save()
            
            messages.success(request, _("Fantastic. You've taken the first step!"))
            
            return HttpResponseRedirect(reverse('archimedes_step2',
                                                args=(patient.patient_id,)))
                            
        else:
            return render_to_response("generic/bootstrapform.html",
                              RequestContext(request,
                                             {'form': form,
                                              'name': _("Step 1 - Please provide some basic information."),
                                              }))
    
    
    #Just a GET Display and unbound form
    return render_to_response("generic/bootstrapform.html",
                             {'name': _("Step 1 - Please Provide Some Basic Information."),
                              'submit_button_text': "Go On",
                              'form': ArchimedesRequiredForm(),},
                              context_instance = RequestContext(request))


def archimedes_step2(request, patient_id):
    name = _('Step 2 - Please Tell Us a Little More.')
    
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)

    if request.method == 'POST':
        form =  ArchimedesStep2Form(request.POST, instance = patient)
        
        if form.is_valid():  
            patient_id = form.save()
            if request.POST['have_bp_chol_info'] == "yes":
                return HttpResponseRedirect(reverse('archimedes_bp_and_cholesterol',
                                                args=(patient.patient_id,)))
            
            
            
            return HttpResponseRedirect(reverse('archimedes_dashboard_or_pharmacy',
                                                args=(patient.patient_id,)))

        else:
            return render_to_response("generic/bootstrapform.html",
                              RequestContext(request,
                                             {'form': form,
                                             'name':name}))
    
    #Just a GET Display a bound form
    return render_to_response("generic/bootstrapform.html",
                             {'name': name,
                              'form': ArchimedesStep2Form(instance=patient),},
                              context_instance = RequestContext(request))



def archimedes_dashboard_or_pharmacy(request, patient_id):
    
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)
    return render_to_response("riskassessments/dashboard-or-pharmacy.html",
                             {'patient': patient,},
                              context_instance = RequestContext(request))
    



def archimedes_bp_and_cholesterol(request, patient_id):
    name = _('Step 3 - Provide Your Blood Pressure and Cholesterol Numbers.')
    
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)

    if request.method == 'POST':
        form = ArchimedesBloodPressureAndCholesterolForm(request.POST,
                                                         instance=patient)
        
        if form.is_valid():  
            patient_id = form.save()
            
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(patient.patient_id,)))

        else:
            return render_to_response("generic/bootstrapform.html",
                              RequestContext(request,
                                             {'form': form,
                                             'name':name}))
    
    #Just a GET Display a bound form
    return render_to_response("generic/bootstrapform.html",
            {'name': name,
            'form': ArchimedesBloodPressureAndCholesterolForm(instance=patient),},
            context_instance = RequestContext(request))
    
def archimedes_basic_info(request, patient_id):
    
    patient = get_latest_object_or_404(ArchimedesRiskAssessment,
                                       patient_id=patient_id)

    if request.method == 'POST':
        form =  ArchimedesBasicInfoForm(request.POST, instance=patient)

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
                             {'name': "Basic Information",
                              'submit_button_text': "Go On",
                              'form': ArchimedesBasicInfoForm(instance=patient),},
                              context_instance = RequestContext(request))




def archimedes_blood_pressure(request, patient_id):
    name = _("Enter Your Blood Pressure Information.")
    
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
                                             { 'name': name,
                                                'form': form,}))
    
    #Just a GET Display a bound form
    return render_to_response("generic/bootstrapform.html",
                             {'name': name,
                              'form': ArchimedesBloodPressureForm(instance=patient),},
                              context_instance = RequestContext(request))




def archimedes_cholesterol(request, patient_id):
    name = _("Enter Your Cholesterol Information")
    
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
                                             {'form': form,
                                              'name': name,}))
    
    
    #Just a GET Display a bound form
    return render_to_response("generic/bootstrapform.html",
                        {'name': name,
                        'form': ArchimedesCholesterolForm(instance=patient),},
                              context_instance = RequestContext(request))



def archimedes_diabetes(request, patient_id):
    name = _("Enter Your Diabetes Information")
    
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
                                             {'form': form,
                                              "name": name}))
    
    
    #Just a GET Display a bound form
    return render_to_response("generic/bootstrapform.html",
                        {'name': name,
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
                                             {'form': form,
                                              'name': _("Additional Information")}))
    
    #Just a GET Display and unbound form
    return render_to_response("generic/bootstrapform.html",
                        {'name': _("Additional Information"),
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