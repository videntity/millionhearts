#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from django.contrib.localflavor.us.models import PhoneNumberField
from sms_utils import send_sms_twilio
import string
import random
from ..locations.models import LocationSetup
import uuid
from emails import send_password_reset_url_via_email



class ValidPasswordResetKey(models.Model):
    user               = models.ForeignKey(User)
    reset_password_key = models.CharField(max_length=50, blank=True)
    expires            = models.DateTimeField(default=datetime.now)


    def __unicode__(self):
        return '%s for user %s expires at %s' % (self.reset_password_key,
                                                 self.user.username,
                                                 self.expires)

    def save(self, **kwargs):

        self.reset_password_key=str(uuid.uuid4())
        now = datetime.now()
        expires=now+timedelta(minutes=settings.SMS_LOGIN_TIMEOUT_MIN)
        self.expires=expires

        #send an email with reset url
        x=send_password_reset_url_via_email(self.user, self.reset_password_key)
        super(ValidPasswordResetKey, self).save(**kwargs)


CONTACT_CHOICES = (('phone','Phone'),('sms','Text Message'),('email','Email'))

class UserProfile(models.Model):
    user                    = models.ForeignKey(User, unique=True)
    pin                     = models.CharField(max_length=4, blank=True, default="")
    mobile_phone_number     = PhoneNumberField(max_length=15, blank=True)
    patient_id              = models.CharField(max_length=20,) #editable=False
    twitter                 = models.CharField(max_length=20, blank=True, default="")
    preferred_contact_method = models.CharField(max_length=5,
                                choices = CONTACT_CHOICES)

    def __unicode__(self):
        return '%s %s (%s)' % (self.user.first_name, self.user.last_name,
                               self.patient_id)
        