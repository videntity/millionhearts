#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=
from django.db import models
from ..intake.models import PatientProfile
from django.contrib.auth.models import User
import datetime
from datetime import timedelta
from ..tracker.models import idTransaction
from ..tracker.utils import jsonify_extra_fields

affirmative_list=["y", "yes", "ok", "k", "si", "1", "did", "didit", "done"]

def a_year_from_today():
    return datetime.date.today() + timedelta(days=366)


class SMSAppointmentReminder(models.Model):
    patient                 = models.ForeignKey(PatientProfile)
    worker                  = models.ForeignKey(User)
    creation_date           = models.DateField(default=datetime.date.today) 
    reminder_datetime       = models.DateTimeField()
    message                 = models.CharField(max_length=140)
    sent                    = models.BooleanField(default=False)
    name                    = models.CharField(max_length=140, blank=True,
                                               null=True)
    def __unicode__(self):
        return '%s %s (%s) will get a reminder at %s' % (self.patient.first_name,
                               self.patient.last_name, self.patient.patient_id,
                               self.reminder_datetime )
        
    class Meta:
        get_latest_by = "-reminder_datetime"
        ordering = ('-reminder_datetime',)




class SMSAdherenceReminder(models.Model):
    """
    This model's job is to define the schedule for a members adherence reminder.
    The information in the model is quereied 1x per day to load the day's
    adherence reminders which are stored in SMSAdherence transaction
    """
    
    patient                 = models.ForeignKey(PatientProfile)
    worker                  = models.ForeignKey(User)
    title                   = models.CharField(max_length=100)
    creation_date           = models.DateField(default=datetime.date.today) 
    reminder_time           = models.TimeField()
    message                 = models.CharField(max_length=140)
    start_date              = models.DateField(default=datetime.date.today)
    end_date                = models.DateField(default=a_year_from_today)
    monday                  = models.BooleanField(default=True)
    tuesday                 = models.BooleanField(default=True)
    wednesday               = models.BooleanField(default=True)
    thursday                = models.BooleanField(default=True)
    friday                  = models.BooleanField(default=True)
    saturday                = models.BooleanField(default=True)
    sunday                  = models.BooleanField(default=True)
   
    def dow(self):
        dowstr=""
        if self.sunday:
            dowstr=dowstr + "S,"
        if self.monday:
            dowstr=dowstr + "M,"        
        if self.tuesday:
            dowstr=dowstr + "T,"
        if self.wednesday:
            dowstr=dowstr + "W,"            
        if self.thursday:
            dowstr=dowstr + "R,"            
        if self.friday:
            dowstr=dowstr + "F,"
        if self.saturday:
            dowstr=dowstr + "S,"            
        if dowstr.endswith(","):
            dowstr=dowstr[:-1]
        return dowstr
   
    def __unicode__(self):
        return 'Reminder %s will be sent to %s %s at %s.' % (
                                self.title,
                                self.patient.first_name,
                                self.patient.last_name,
                                self.reminder_time)
        
    class Meta:
        get_latest_by = "-creation_date"
        ordering = ('-creation_date',)
        



class SMSAdherenceTransaction(models.Model):
    """
    This model holds info on a per message basis. A cron process will load
    these nightly and another process will update the record if and when a
    response is received.
    """
    idtransaction        = models.ForeignKey(idTransaction, blank=True,
                                            null = True, editable=False)
    twilio_id            = models.CharField(max_length = 50,blank=True,
                                            null = True)
    schedule             = models.ForeignKey(SMSAdherenceReminder)
    reminder_time        = models.TimeField(blank = True, null = True)
    reminder_date        = models.DateField(default = datetime.date.today)
    initial_create       = models.BooleanField(default = True)
    sent                 = models.BooleanField(default = False)
    response_received    = models.BooleanField(default = False)
    affirmative_response = models.BooleanField(default = False)
    response_text        = models.CharField(max_length=140, blank=True,
                                            null=True)
    creation_dt         = models.DateTimeField(auto_now_add=True)
    creation_date       = models.DateField(default=datetime.date.today())
    
    class Meta:
        get_latest_by = "-creation_date"
        ordering = ('-creation_date',)
        unique_together = (('schedule','reminder_date'),)
    
    def __unicode__(self):
        return 'Message for %s. Sent=%s, Response=%s affirmative=%s' % (
                                self.schedule.patient, self.sent,
                                self.response_received,
                                self.affirmative_response)            
    def save(self, **kwargs):
        today=datetime.date.today()
        #Create/Update a RESTCAT tx
        extra_fields = jsonify_extra_fields(self)
        
        
        #if we are creating this for later execution
        if self.initial_create==True and \
            ((self.schedule.sunday   and 7==today.isoweekday()) or \
            (self.schedule.monday    and 1==today.isoweekday()) or \
            (self.schedule.tuesday   and 2==today.isoweekday()) or \
            (self.schedule.wednesday and 3==today.isoweekday()) or \
            (self.schedule.thursday  and 4==today.isoweekday()) or \
            (self.schedule.friday    and 5==today.isoweekday()) or \
            (self.schedule.saturday  and 6==today.isoweekday())):
            
            #create the restcat tranaction
            if not self.idtransaction:
                from ..tracker.models import idTransaction
                self.idtransaction=idTransaction.objects.create(
                                        subject=self.schedule.patient,
                                        sender=self.schedule.worker,
                                        receiver=self.schedule.worker,
                                        extra_fields=jsonify_extra_fields(self))    
            
            
            self.initial_create=False 
            self.reminder_time = self.schedule.reminder_time
            super(SMSAdherenceTransaction, self).save(**kwargs)
        #if the message was sent and a response was received.
        elif self.sent==True and self.response_received==True and \
                self.response_text:
            #set affirmative to true if affirmative response received.
            for a in affirmative_list:
                if  str(self.response_text).lower().startswith(a):
                    self.affirmative_response=True
            
            #Check to see if the record has been updated.
            if str(self.idtransaction.extra_fields) !=  str(extra_fields):
                self.idtransaction.extra_fields = extra_fields
                self.idtransaction.save()
            
            super(SMSAdherenceTransaction, self).save(**kwargs)
        # if we are updating the sent status
        elif self.initial_create==False:
            
            
            
            
            
            super(SMSAdherenceTransaction, self).save(**kwargs)