#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=

from django.db import models
from ..intake.models import PatientProfile
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.localflavor.us.us_states import US_STATES
from django.contrib.localflavor.us.models import PhoneNumberField
import datetime
from ..tracker.utils import jsonify_extra_fields
from ..tracker.models import idTransaction
from ..organizations.models import Organization

REFERRAL_TYPE_CHOICES =(('clothing','Clothing'),
                    ('confirmatory-testing','Confirmatory Testing'),
                    ('crcs','CRCS'),
                    ('eis-services','EIS-Services'),
                    ('food','Food'),
                    ('furniture','Furniture'),
                    ('hep-c-information','Hepatits C Information'),
                    ('hepatitis-screening','Hepatits Screening'),
                    ('housing','Housing'),
                    ('individual-group-counseling','Individual Group Counseling'),
                    ('mental-health-services','Mental Health Services'),
                    ('needle-exchange','Needle Exchange'),
                    ('pcrs','PCRS'),
                    ('primary-care','Primary Care'),
                    ('rental-utility-assistance-service','Rental / Utility Assistance'),
                    ('std-screening','STD Screening'),
                    ('substance-abuse-treatment','Substance Abuse Treatment'),
                    ('support-services','Support Services'),
                    )



TRANSPORTATION_CHOICES=(('NOT-APPLICABLE','Not Applicable'),
                ('AUTOMOBILE','Automobile'),
                ('FOOT','Foot'),
                ('PUBLIC-TRANSIT','Public Transit'),)

LINK_TYPE_CHOICES =(('UNKNOWN','Unknown'),
                    ('NEW','New'),
                    ('RE-LINK','Re-Link'),)


TFYN_CHOICES = ((False,"No"),(True, "Yes"))



class Referral(models.Model):
    idtransaction        = models.ForeignKey('tracker.idTransaction', blank=True,
                                            null = True, editable=False)
    patient             = models.ForeignKey(PatientProfile)
    worker              = models.ForeignKey(User)
    referral_type       = models.CharField(max_length = 100,
                                           choices=REFERRAL_TYPE_CHOICES)
    organization        = models.ForeignKey(Organization)

    ok_to_mail          = models.BooleanField(default=False, choices = TFYN_CHOICES,
                                            verbose_name='Is it okay to mail this person?')
    okay_to_call        = models.BooleanField(default=False,  choices = TFYN_CHOICES,
                                            verbose_name='Is it okay to call this person?')
    okay_to_leave_message = models.BooleanField(default=False,  choices = TFYN_CHOICES,
                                            verbose_name='Is it okay to leave a message by phone with another person?')
    note                = models.TextField(max_length = 1000,
                                           blank=True,
                                           default="")
    cpt_code            = models.CharField(max_length = 30,
                                           blank=True, null=True)
    icd9_code           = models.CharField(max_length = 30,
                                           blank=True, null=True)
    icd10_code          = models.CharField(max_length = 30,
                                           blank=True, null=True)

    creation_date        = models.DateField(default=datetime.date.today)
    
    def __unicode__(self):
        return '%s was referred to %s for %s on %s by %s %s' % (self.patient,
                                            self.organization,
                                            self.referral_type,  
                                            self.creation_date,
                                            self.worker.first_name,
                                            self.worker.last_name)
        

    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)

    def save(self, **kwargs):        
        #Create/Update a RESTCAT tx
        extra_fields = jsonify_extra_fields(self)
        if not self.idtransaction:
            self.idtransaction=idTransaction.objects.create(subject=self.patient,
                                        sender=self.worker,
                                        receiver=self.worker,
                                        extra_fields=jsonify_extra_fields(self))
            super(Referral, self).save(**kwargs)
        else:
            #Check to see if the record has been updated.
            extra_fields = jsonify_extra_fields(self)
            if str(self.idtransaction.extra_fields) !=  str(extra_fields):
                self.idtransaction.extra_fields = extra_fields
                self.idtransaction.save()
        super(Referral, self).save(**kwargs)
    
    
class Linkage(models.Model):
    
    idtransaction        = models.ForeignKey('tracker.idTransaction', blank=True,
                                            null = True, editable=False)
    patient             = models.ForeignKey(PatientProfile)
    worker              = models.ForeignKey(User)
    creation_date       = models.DateField(default=datetime.date.today)
    linkage_date        = models.DateField(default=datetime.date.today) 
    link_type           = models.CharField(max_length = 30,
                                           choices=LINK_TYPE_CHOICES,
                                           default="UNKNOWN")
    referral_type       = models.CharField(max_length = 100,
                                           verbose_name ="Linkage Type",
                                           choices=REFERRAL_TYPE_CHOICES)
    organization            = models.ForeignKey(Organization)
    mode_of_transportation  = models.CharField(max_length=50,
                                               choices=TRANSPORTATION_CHOICES)
    
    time_traveling_pickup_minutes   = models.PositiveIntegerField(max_length=3)
    time_traveling_return_minutes   = models.PositiveIntegerField(max_length=3)
    time_at_med_facility_minutes    = models.PositiveIntegerField(max_length=3)
    personnel_expense               = models.FloatField(max_length=10, default=0.0)
    mileage                         = models.PositiveIntegerField(max_length=5,
                                                                  blank=True,
                                                                  default=0)
    
    ok_to_mail          = models.BooleanField(default=False, choices = TFYN_CHOICES,
                                            verbose_name='Is it okay to mail this person?')
    okay_to_call        = models.BooleanField(default=False,  choices = TFYN_CHOICES,
                                            verbose_name='Is it okay to call this person?')
    okay_to_leave_message = models.BooleanField(default=False,  choices = TFYN_CHOICES,
                                            verbose_name='Is it okay to leave a message by phone with another person?')
    
    note                = models.TextField(max_length = 1000,
                                           blank=True,
                                           default="")
    cpt_code            = models.CharField(max_length = 30,
                                           blank=True, default="")
    cpt_modifier_codes  = models.CharField(max_length = 256,
                                           blank=True, default="")

    icd9_code           = models.CharField(max_length = 32,
                                           blank=True, default="")
    icd10_code          = models.CharField(max_length = 32,
                                           blank=True, default="")

    def __unicode__(self):
        return u'%s was linked to %s for %s on %s via %s by %s %s ' % (self.patient,
                                            self.organization,
                                            self.referral_type,  
                                            self.creation_date,
                                            self.mode_of_transportation,
                                            self.worker.first_name,
                                            self.worker.last_name)  

    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        
        
    def save(self, **kwargs):
        #Create/Update a RESTCAT tx
        #extra_fields = jsonify_extra_fields(self)
        #if not self.idtransaction:
        #    self.idtransaction=idTransaction.objects.create(subject=self.patient,
        #                                sender=self.worker,
        #                                receiver=self.worker,
        #                                extra_fields=jsonify_extra_fields(self))
        #    super(Linkage, self).save(**kwargs)
        #else:
        #    #Check to see if the record has been updated.
        #    extra_fields = jsonify_extra_fields(self)
        #    if str(self.idtransaction.extra_fields) !=  str(extra_fields):
        #        self.idtransaction.extra_fields = extra_fields
        #        self.idtransaction.save()
                
        super(Linkage, self).save(**kwargs)

LINK_FOLLOWUP_STATUS_CHOICES =(
    ('ACTIVELY-TRACKED-IN-CARE','Actively-Tracked - Client In Care'),
    ('ACTIVELY-TRACKED-NOT-IN-CARE','Actively-Tracked - Client NOT In Care'),
    ('TRACKING-TERMINATED-12-MONTHS-IN-CARE)','Tracking Terminated after 12 months. Client in Care'),
    ('TRACKING-TERMINATED-12-MONTHS-NOT-IN-CARE)','Tracking Terminated after 12 months. Client NOT in Care'),
    ('TRACKING-TERMINATED-DECEASED-)','Tracking Terminated - Client Deceased'),
    ('INCARCERATED)','Client Incarcerated'),
    )


ACTIVITY_TYPE_CHOICES =(('IN-PERSON','In person'),
                        ('BY-PHONE','By Phone'),)


SERVICE_CHOICES = (('APPOINTMENT-REMINDER','Appointment reminder'),
    ('CONFIRMATORY-NOTIFICATION','Confirmatory notification'),
    ('TRANSPORT-TO-MEDICAL-APPOINTMENT','Transportation to medical appointment'),
    ('TRANSPORT-FOR-CONFIRMATORY-HIV-TEST','Transportation to confirmatory testing'),
    ('TRANSPORT-FOR-DOCUMENTATION','Transportation to secure documentation to access services'),
    ('OTHER','Other')
    )





DETERMINATION_CHOICES = (
    ('COMPLETE','Complete'),
    ('CLIENT-UNAVAILABLE','Client unavailable'),
    ('CLIENT-DECLINED','Client declined service'),
    ('CALLED-NO-ANSWER','Called but no answer'),
    ('CALLED-DISCONNECTED-PHONE','Called but phone was disconnected'),
    ('CLIENT-INCARCERATED','Client Incarcerated'),
    ('CLIENT-DECEASED','Client Deceased'),
    ('INCOMPLETE','Incomplete'),
)



BOOL_CHOICES = ((True, "Yes"),(False, "No"))

class LinkageFollowUp(models.Model):
    linkage                         = models.ForeignKey(Linkage)
    worker                          = models.ForeignKey(User)
    creation_date                   = models.DateField(default=datetime.date.today)
    linkage_status                  = models.CharField(choices=LINK_FOLLOWUP_STATUS_CHOICES,
                                            max_length=60)
    activity_type                   = models.CharField(choices=ACTIVITY_TYPE_CHOICES,
                                            max_length=30)
    service                         = models.CharField(choices=SERVICE_CHOICES,
                                            max_length=60)
    service_other                   = models.CharField(blank=True, default="",
                                            max_length=30)
    determination                   = models.CharField(choices=DETERMINATION_CHOICES,
                                            max_length=30)
    time_on_phone_minutes           = models.PositiveIntegerField(max_length=3)
    time_traveling_pickup_minutes   = models.PositiveIntegerField(max_length=3)
    time_traveling_return_minutes   = models.PositiveIntegerField(max_length=3)
    time_at_med_facility_minutes    = models.PositiveIntegerField(max_length=3)
    personnel_expense               = models.FloatField(max_length=10, default=0.0)
    mileage                         = models.PositiveIntegerField(max_length=5,
                                                                  blank=True,
                                                                  default=0)
    
    
    
    cpt_code            = models.CharField(max_length = 30,
                                           blank=True, default="")
    cpt_modifier_codes  = models.CharField(max_length = 256,
                                           blank=True, default="")

    icd9_code           = models.CharField(max_length = 32,
                                           blank=True, default="")
    icd10_code          = models.CharField(max_length = 32,
                                           blank=True, default="")
    
    sex_active_last_30 = models.BooleanField(default=False, choices=BOOL_CHOICES,
                            blank=True,
                            verbose_name="Have you been sexually active within the last 30 days?")
    
    did_client_use_condom = models.BooleanField(default=False, choices=BOOL_CHOICES,
                                blank=True,
                                verbose_name="Did you use a condom or other protection?")
    
    did_client_get_high =   models.BooleanField(default=False, choices=BOOL_CHOICES,
                                blank=True,
                                verbose_name="Did you get high, drink, or shoot up in the last 30 days?")
    
    note                 = models.TextField(max_length = 2048, default="",
                                            blank=True)

    
    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        
    def __unicode__(self):
        return '%s %s performed a/an %s linkage follow-up %s on %s' % (
                                self.worker.first_name, self.worker.last_name,
                                self.service, self.activity_type,
                                self.creation_date) 