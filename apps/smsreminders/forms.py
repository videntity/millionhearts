#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4


from django.forms import ModelForm
from django import forms
from models import *
import datetime
from datetime import timedelta
from utils import send_sms_twilio
    

class SMSSendForm(forms.Form):
    to      = forms.CharField()
    message = forms.CharField()
    
    def save(self):
        send_sms_twilio(self.cleaned_data['message'],
                        self.cleaned_data['to'])
