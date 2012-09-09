#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.db import models
from ..intake.models import PatientProfile
from django.contrib.auth.models import User
#from datetime import datetime
from django.conf import settings
from django.contrib.localflavor.us.us_states import US_STATES
from django.contrib.localflavor.us.models import PhoneNumberField
import datetime
from datetime import timedelta, date


BOOL_CHOICES = ((True, "YES"),(False, "No"))

class FormName(models.Model):
    form_name = models.CharField(max_length=200,blank=True, null=True)
    active =    models.BooleanField(choices=BOOL_CHOICES, default=False,
        verbose_name="Live Form")

    def __unicode__(self):
        return '%s' % (self.form_name)

    class Meta:
        get_latest_by = "form_name"
        ordering = ('form_name',)


class ExtraFormContent(models.Model):

    form_name       = models.ForeignKey('FormName')
    field_name      = models.CharField(max_length=200)
    field_pre_text  = models.TextField()
    field_post_text = models.TextField()

    def __unicode__(self):
        return '%s.%s' % (self.form_name, self.field_name)

    class Meta:
        get_latest_by = "form_name"
        ordering = ('field_name',)
