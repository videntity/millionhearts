#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime

from django.forms import ModelForm
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from apps.widgets import ClientSignatureWidget
from models import *
import datetime




class ArchimedesRiskAssessmentForm(ModelForm):
    class Meta:
        model = ArchimedesRiskAssessment
        exclude = ('creation_date', 'trackingid')
    required_css_class = 'required'




class ADAType2DiabetesScreenForm(ModelForm):
    class Meta:
        model = ADAType2DiabetesScreen
        exclude = ('patient','worker',)
    creation_date=forms.DateField(initial = datetime.date.today,
                                  widget  = SelectDateWidget())
    required_css_class = 'required'
    

class CAGEAIDSubstanceAbuseScreenForm(ModelForm):
    class Meta:
        model = CAGEAIDSubstanceAbuseScreen
        exclude = ('patient','worker',)
    creation_date=forms.DateField(initial = datetime.date.today,
                                  widget  = SelectDateWidget())
    required_css_class = 'required'



    
    


class Framingham10yrHeartRiskTestForm(ModelForm):
    class Meta:
        model = Framingham10yrHeartRiskTest
        exclude = ('patient','worker', 'points', 'percent_risk')
    creation_date=forms.DateField(initial = datetime.date.today,
                                   widget = SelectDateWidget())
    required_css_class = 'required'
    
    
    def clean_age(self):
        age = self.cleaned_data.get("age", "")
        if 20 <= age <= 79:
            return int(age)
        raise forms.ValidationError("Age must be between 20 and 79.")
    
    def clean_total_cholesterol(self):
        total_cholesterol = self.cleaned_data.get("total_cholesterol", "")
        if 130 <= total_cholesterol <= 320:
            return int(total_cholesterol)
        raise forms.ValidationError("Total cholesterol must be between 130 and 320.")
    
    def clean_hdl_cholesterol(self):
        hdl_cholesterol = self.cleaned_data.get("hdl_cholesterol", "")
        if 20 <= hdl_cholesterol <= 100:
            return int(hdl_cholesterol)
        raise forms.ValidationError("HDL cholesterol must be between 20 and 100.")
    
    def clean_systolic_blood_pressure(self):
        systolic_blood_pressure = self.cleaned_data.get("systolic_blood_pressure", "")
        if 90 <= systolic_blood_pressure <= 200:
            return int(systolic_blood_pressure)
        raise forms.ValidationError("Systolic blood pressure must be between 90 and 200.")





class CardioDiabetesRiskTestForm(ModelForm):
    class Meta:
        model = CardioDiabetesRiskTest
        exclude = ('patient','worker', 'points', 'risk_list')
    creation_date=forms.DateField(initial = datetime.date.today,
                                   widget = SelectDateWidget())
    required_css_class = 'required'
