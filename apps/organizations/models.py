#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=

from django.db import models
from django.contrib.localflavor.us.us_states import US_STATES
from django.contrib.localflavor.us.models import PhoneNumberField
from ..intake.models import PatientProfile
from django.contrib.auth.models import User
import datetime


class Service(models.Model):
    name    = models.CharField(max_length = 200,unique=True)
    slug    = models.CharField(max_length = 200,unique=True)

    def __unicode__(self):
        s = '%s' % (self.name)
        return s

    class Meta:
        ordering = ('slug',)  
 

ORG_TYPE_CHOICES =( ('FREE-CLINIC',         'Free Clinic'),
                    ('COM-PAYER',           'Insurance Company or HMO'),
                    ('FED-GOV-PAYER',       'Federal Government Payer'),
                    ('STATE-GOV-PAYER',     'State Government Payer'),
                    ('LOCAL-GOV-PAYER',     'Local Government Payer'),
                    ('PROVIDER-HOSPITAL',   'Hospital'),
                    ('PROVIDER-SPECIALITY', "Doctor Speciality"),
                    ('PROVIDER-PRIMARY',    "Primary Care"),
                    ('FED-GOV',             'Federal Government'),
                    ('STATE-GOV',           'State Government'),
                    ('LOCAL-GOV',           'Local Government'),
                    ('NON-PROFIT',          'Non Profit Organization'),
                    ('FAITH-NON-PROFIT',    'Faith-Based Organization'),
                    )


class Organization(models.Model):
    name            = models.CharField(max_length = 200,unique=True)
    slug            = models.CharField(max_length = 200, unique=True)
    #npi             = models.CharField(max_length = 20, blank=True, default="")
    org_type        = models.CharField(max_length=50, choices=ORG_TYPE_CHOICES)
    accepts_insurance  = models.ManyToManyField('self', blank=True,
                                             related_name='insurance')
    services        = models.ManyToManyField(Service, blank=True,
                                             related_name='organization_services')
    address1        = models.CharField(max_length = 200)
    address2        = models.CharField(max_length = 100, blank=True, default="")
    city            = models.CharField(max_length = 100)
    state           = models.CharField(max_length=2, choices=US_STATES,
                                       default="DC")
    zip             = models.CharField(max_length = 10)
    phone_1         = PhoneNumberField(max_length = 15, blank=True,   default="")
    phone_2         = PhoneNumberField(max_length = 15, blank=True,   default="")
    note            = models.TextField(max_length = 1000, blank=True, default="")
    verified                        = models.BooleanField(default=False)
    is_accepting_new_clients        = models.BooleanField(default=False)
    contact_person  = models.CharField(max_length = 100, blank=True,  default="")
    url             = models.CharField(max_length = 500, blank=True,  default="")
    description     = models.CharField(max_length = 100, blank=True,  default="")
    creation_date   = models.DateField(default=datetime.date.today)    
    
    
    def __unicode__(self):     
        return self.name

    class Meta:
        ordering = ('slug',)
        


class Provider(models.Model):
    first_name      = models.CharField(max_length = 200)
    last_name       = models.CharField(max_length = 200)
    organization    = models.ForeignKey(Organization, blank=True, null=True)
    npi             = models.CharField(max_length = 20, blank=True, default="")
    address1        = models.CharField(max_length = 200)
    address2        = models.CharField(max_length = 100, blank=True, default="")
    city            = models.CharField(max_length = 100)
    state           = models.CharField(max_length = 2, choices=US_STATES,
                                       default="DC")
    zip             = models.CharField(max_length = 10)
    phone_1         = PhoneNumberField(max_length = 15, blank=True,   default="")
    phone_2         = PhoneNumberField(max_length = 15, blank=True,   default="")
    fax_number      = PhoneNumberField(max_length = 15, blank=True,   default="")
    note            = models.TextField(max_length = 1000, blank=True, default="")
    verified        = models.BooleanField(default=False)
    is_accepting_new_clients        = models.BooleanField(default=False)
    contact_person  = models.CharField(max_length = 100, blank=True,   default="")
    url             = models.CharField(max_length = 500, blank=True,  default="")
    description     = models.CharField(max_length = 100, blank=True,  default="")
    individual      = models.BooleanField(default=False)
    group           = models.BooleanField(default=False)
    code            = models.CharField(max_length = 20, blank=True,  default="")
    
    taxclass =  models.CharField(max_length = 20, blank=True,  default="")
    speciality=  models.CharField(max_length = 100, blank=True,  default="")
    
    creation_date   = models.DateField(default=datetime.date.today)    
    
    
    def __unicode__(self):     
        s = '%s, %s (%s)' % (self.last_name, self.first_name, self.description)
        return s

    class Meta:
        ordering = ('last_name', 'first_name')





class PatientCareTeam(models.Model):
    patient             = models.ForeignKey(PatientProfile, unique=True)
    primary_provider    = models.ForeignKey(Provider, blank=True, null=True)
    providers           = models.ManyToManyField(Provider, blank=True,
                                related_name='patient_care_team_providers')
    organizations       = models.ManyToManyField(Organization, blank=True,
                                related_name='patient_care_team_organiztions')
    users               = models.ManyToManyField(User, blank=True,
                                related_name='patient_care_team_others')
    notes               = models.TextField(max_length=1024, blank=True,
                                           default="")
    creation_date       = models.DateField(default=datetime.date.today)

    class Meta:
        ordering = ('patient', 'creation_date')
        
    def __unicode__(self):     
        s = "%s %s's primary care provider is %s" % ( self.patient.first_name,
                                                        self.patient.last_name,
                                                        self.primary_provider,)
        return s
    
    def save(self, **kwargs):
        if self.primary_provider:
            self.patient.has_medical_home=True
            self.patient.save()
        super(PatientCareTeam, self).save(**kwargs)
        
    