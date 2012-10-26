#vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.db import IntegrityError
from ..intake.models import PatientProfile
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from datetime import datetime
from ..accounts.decorators import access_required
from forms import *
from ..intake.forms import PatientSearchForm
from models import *
from utils import get_messages, send_sms_twilio, process_adherence_responses
from ..utils import build_pretty_data_view
from datetime import datetime, date
from time import gmtime, strftime
import json, sys

def cron_insert_todays_reminders(request, cron_key):
    if cron_key != settings.CRON_KEY:
        return HttpResponse("Forbidden", status=401)
        
    # Create all of today's reminders
    # This runs 1x per day at midnight.
    # SMSAdherenceTransaction
    today=date.today()
    rs = SMSAdherenceReminder.objects.filter(start_date__lte=today,
                                             end_date__gte=today)
    
    inserted_reminder_list=[]
    #
    #print "cron insert with "+cron_key
    #print "inserted_reminders_list:"
    #print inserted_reminder_list
    #print "filtered reminders for today"
    ##print rs
    ##
    for i in rs:
        if ((i.sunday    and 7==today.isoweekday()) or \
            (i.monday    and 1==today.isoweekday()) or \
            (i.tuesday   and 2==today.isoweekday()) or \
            (i.wednesday and 3==today.isoweekday()) or \
            (i.thursday  and 4==today.isoweekday()) or \
            (i.friday    and 5==today.isoweekday()) or \
            (i.saturday  and 6==today.isoweekday())):
            #Add check to ensure this is new.
            try:
                SMSAdherenceTransaction.objects.create(schedule=i)
                inserted_reminder_list.append(str(i))
            except(IntegrityError):
                print "integrity error"
                print sys.exc_info()


        
    #Otherwise there was nothing to process.
    
    jsonstr={"code": "200",
             "message": "The following reminders have been scheduled for today. This script should be run 1x/night in the early morning (after midnight)",
             "transaction_datetime" : strftime("%Y-%m-%d %H:%M:%S", gmtime()), 
             "results": inserted_reminder_list}
                
            
    jsonstr=json.dumps(jsonstr, indent = 4,)
    return HttpResponse(jsonstr, mimetype="text/plain")



def cron_process_adherence_responses(request, cron_key):
    if cron_key != settings.CRON_KEY:
        return HttpResponse("Forbidden", status=401)
    results =process_adherence_responses()
    jsonstr={"code": "200",
            "message": "Adherence transaction responses processed. Here is the list",
                     "transaction_datetime" : strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                     "results": results}
                
    jsonstr=json.dumps(jsonstr, indent = 4,)
    return HttpResponse(jsonstr, mimetype="text/plain")
    

def cron_adherence_send(request,cron_key):       
    if cron_key != settings.CRON_KEY:
        return HttpResponse("Forbidden", status=401)
    
    a = SMSAdherenceTransaction.objects.filter(sent=False,
                                          reminder_time__lte=datetime.now())
    twilio_tx_list=[]
    if a:
        for i in a:
            d=send_sms_twilio(i.schedule.message,
                                   i.schedule.patient.mobile_phone_number)
            i.twilio_id=d['twilio_id']
            twilio_tx_list.append(d)
            i.sent=True
            i.save()
            
    jsonstr={"code": "200",
            "message": "Adherence transactions sent. Here is the list",
            "transaction_datetime" : strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            "results": twilio_tx_list}
                
    jsonstr=json.dumps(jsonstr, indent = 4,)
    return HttpResponse(jsonstr, mimetype="text/plain")
    
    #Otherwise there was nothing to process.
    jsonstr={"code": "200",
             "message": "No adherence transactions were required to be sent at this time",
             "transaction_datetime" : strftime("%Y-%m-%d %H:%M:%S", gmtime()), 
             "results": ()}
                
    jsonstr=json.dumps(jsonstr, indent = 4,)
    return HttpResponse(jsonstr, mimetype="text/plain")


def cron_appointment_send(request, cron_key):       
    if cron_key != settings.CRON_KEY:
        return HttpResponse("Forbidden", status=401)
    
    a = SMSAppointmentReminder.objects.filter(sent=False,
                                          reminder_datetime__lte=datetime.now())
    twilio_tx_list=[]
    if a:
        for i in a:
            d=send_sms_twilio(i.message,
                                   i.patient.mobile_phone_number)
            i.name=d['twilio_id']
            twilio_tx_list.append(d)
            i.sent=True
            i.save()
            
    jsonstr={"code": "200",
            "message": "Appointment transactions sent. Here is the list",
            "transaction_datetime" : strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            "results": twilio_tx_list}
                
    jsonstr=json.dumps(jsonstr, indent = 4,)
    return HttpResponse(jsonstr, mimetype="text/plain")
    
    #Otherwise there was nothing to process.
    jsonstr={"code": "200",
             "message": "No adherence transactions were required to be sent at this time",
             "transaction_datetime" : strftime("%Y-%m-%d %H:%M:%S", gmtime()), 
             "results": ()}
                
    jsonstr=json.dumps(jsonstr, indent = 4,)
    return HttpResponse(jsonstr, mimetype="text/plain")


@login_required
def sms_send(request):       
    if request.method == 'POST':
    
        form = SMSSendForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "SMS Sent.")
            return render_to_response('smsreminders/send.html', 
                             {'form': SMSSendForm()},
                                context_instance = RequestContext(request))
        #the form has errors
        return render_to_response('generic/bootstrapform.html', 
                             {'form': form},
                                context_instance = RequestContext(request))
    
    #request is a GET (not a POST)    
    return render_to_response('generic/bootstrapform.html', 
                             {'form': SMSSendForm()},
                                context_instance = RequestContext(request))






@login_required
@access_required("tester")
def sms_appointment_reminder_create(request, pat_id):       
    pp = get_object_or_404(PatientProfile, patient_id=pat_id)
    from datetime import datetime
    current_reminders=SMSAppointmentReminder.objects.filter(patient=pp,
                            reminder_datetime__gte=datetime.now())
    if request.method == 'POST':
        form = SMSAppointmentReminderForm(request.POST)
        if form.is_valid():
            reminder= form.save(commit=False)
            reminder.patient=pp
            reminder.worker=request.user
            reminder.save()
            messages.success(request, "Successfully added an appointment reminder.")
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(pat_id,)))
        
        else:
            return render_to_response('smsreminders/appointment/create.html',
                        {
                         'form': form,
                         'current_reminders': current_reminders,
                        },RequestContext(request))
        
    else:

        return render_to_response('smsreminders/appointment/create.html',
                                {
                                'form': SMSAppointmentReminderForm(),
                                'current_reminders': current_reminders,
                                },
                            RequestContext(request))# Create your views here.



@login_required
@access_required("tester")
def sms_adherence_search_by_name(request):
    if request.method == 'POST':
    
        form = PatientSearchForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            first_name = data['first_name']
            last_name = data['last_name']
            
            #so do a filter
            pps = PatientProfile.objects.all()
            if last_name:
                pps = pps.filter(last_name__icontains=last_name)
            
            if first_name:
                pps = pps.filter(first_name__icontains=first_name)
                
            #add messages about our results.
            result_count = pps.count()
                    
            if (result_count == 0):
                result_string = "%s results found." % (result_count)
            elif (result_count == 1):
                result_string = "%s result found." % (result_count)
            else:
                result_string = "%s results found" % (result_count)
            return render_to_response('smsreminders/adherence/search-by-name.html', 
                             {'form': PatientSearchForm(),
                              'results': pps,
                              'result_count': result_string},
                              context_instance = RequestContext(request))
            
        #form is invalid    
        return render_to_response('smsreminders/adherence/search-by-name.html', 
                             {'form': form},
                              context_instance = RequestContext(request))
    
    #request is a GET (not a POST)    
    return render_to_response('smsreminders/adherence/search-by-name.html', 
                             {'form': PatientSearchForm()},
                                context_instance = RequestContext(request))





@login_required
@access_required("tester")
def sms_adherence_reminder_create(request, pat_id):       
    pp = get_object_or_404(PatientProfile, patient_id=pat_id)
    current_reminders=SMSAdherenceReminder.objects.filter(patient=pp)
    if request.method == 'POST':
        form = SMSAdherenceReminderForm(request.POST)
        if form.is_valid():
            #success!
            reminder= form.save(commit=False)
            reminder.patient=pp
            reminder.worker=request.user
            reminder.save()
            messages.success(request, "Successfully added an adherence reminder.")
            
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(pat_id,)))
            
        
        else:
            #the form had errors
            return render_to_response('smsreminders/adherence/create.html',
                        {
                         'form': form,
                         'current_reminders': current_reminders,
                        },
                        RequestContext(request))
        
    else:
        #This is a GET
        return render_to_response('smsreminders/adherence/create.html',
                                {
                                'form': SMSAdherenceReminderForm(),
                                'current_reminders': current_reminders,
                                },
                            RequestContext(request))# Create your views her
