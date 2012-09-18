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



class ValidSMSCode(models.Model):
    user               = models.ForeignKey(User)
    sms_code           = models.CharField(max_length=4, blank=True)
    expires            = models.DateTimeField(default=datetime.now)


    def __unicode__(self):
        return '%s for user %s expires at %s' % (self.sms_code,
                                                 self.user.username,
                                                 self.expires)

    def save(self, **kwargs):
        up=self.user.get_profile()
        randcode=random.randint(1000,9999)
        if not self.sms_code:
            if up.mobile_phone_number!='999-999-9999':
                self.sms_code=randcode
            else:
                self.sms_code='9999'
            print self.sms_code

        now = datetime.now()
        expires=now+timedelta(minutes=settings.SMS_LOGIN_TIMEOUT_MIN)
        self.expires=expires
        new_number="+1%s" %(string.replace(str(up.mobile_phone_number),"-", ""))
        #send an sms code
        if up.mobile_phone_number!='999-999-9999':
            x=send_sms_twilio(twilio_body=self.sms_code, twilio_to=new_number)
        else:
            x=''
        super(ValidSMSCode, self).save(**kwargs)


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



class UserProfile(models.Model):
    user                = models.ForeignKey(User, unique=True)
    pin                 = models.CharField(max_length=4, blank=True)
    mobile_phone_number = PhoneNumberField(max_length=15, blank=True)
    patient_id          = models.CharField(max_length=20)
    twitter_handle      = models.CharField(max_length=4, blank=True, default="")

    def __unicode__(self):
        return '%s %s (%s)' % (self.user.first_name, self.user.last_name,
                               self.worker_id)

permission_choices=(    ('provider',  'provider'),
                        ('tester',  'tester'),
                        ('outreach',    'outreach'),
                        ('member_navigator',  'member_navigator'),
                        ('admin',  'admin'),
                        ('reporter',  'reporter'),)

class Permission(models.Model):
    user  = models.ForeignKey(User)
    permission_name = models.CharField(max_length=50,
        choices=permission_choices)

    def __unicode__(self):
        return '%s %s has the %s permission.' % (self.user.first_name,
                                                 self.user.last_name,
                                                 self.permission_name)

    class Meta:
        unique_together = (("user", "permission_name"),)


