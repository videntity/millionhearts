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

from django.utils.translation import ugettext_lazy as _


class ArchimedesRiskAssessmentForm(ModelForm):
    class Meta:
        model = ArchimedesRiskAssessment
        exclude = ('creation_date', 'trackingid', 'archimedes_json_result')
    required_css_class = 'required'


#The first form
class ArchimedesRequiredForm(ModelForm):
    class Meta:
        model = ArchimedesRiskAssessment
        fields = ('sex', 'cholesterolmeds', 'smoker', 'height', 'age', 'weight',)
    required_css_class = 'required'
    
    #sex  = forms.TypedChoiceField(choices = GENDER_CHOICES, initial = None,
    #                              widget=forms.RadioSelect())
    def clean_age(self):
        age     = self.cleaned_data.get("age", "")
        if age:
            if not 18 <= int(age) <= 130:
                raise forms.ValidationError(_("Age must be between 18 and 130 years."))
        return age


    def clean_weight(self):
        weight     = self.cleaned_data.get("weight", "")
        if weight:
            if not 80 <= float(weight) <= 600:
                raise forms.ValidationError(_("Weight must be between 80 and 600 lbs."))
        return weight



class ArchimedesBasicInfoForm(ModelForm):
    class Meta:
        model = ArchimedesRiskAssessment
        fields = ('sex', 'cholesterolmeds', 'smoker', 'height', 'age', 'weight',
                  'diabetes', 'stroke', 'mi', 'bloodpressuremeds',
                  'have_bp_chol_info',
                  
                  )
    required_css_class = 'required'
    
    #sex  = forms.TypedChoiceField(choices = GENDER_CHOICES, initial = None,
    #                              widget=forms.RadioSelect())
    def clean_age(self):
        age     = self.cleaned_data.get("age", "")
        if age:
            if not 18 <= int(age) <= 130:
                raise forms.ValidationError(_("Age must be between 18 and 130 years."))
        return age


    def clean_weight(self):
        weight     = self.cleaned_data.get("weight", "")
        if weight:
            if not 80 <= float(weight) <= 600:
                raise forms.ValidationError(_("Weight must be between 80 and 600 lbs."))
        return weight



#The first form
class ArchimedesStep2Form(ModelForm):
    class Meta:
        model = ArchimedesRiskAssessment
        fields = ('diabetes', 'stroke', 'mi', 'bloodpressuremeds',
                  'have_bp_chol_info',)
    required_css_class = 'required'





class ArchimedesBloodPressureForm(ModelForm):
    class Meta:
        model = ArchimedesRiskAssessment
        fields = ('systolic', 'diastolic',)
    required_css_class = 'required'

    def clean(self):
        cleaned_data  = super(ArchimedesBloodPressureForm, self).clean()
        systolic      = cleaned_data.get("systolic", "")
        diastolic     = cleaned_data.get("diastolic", "")
    
        if systolic and diastolic:
            if int(diastolic) > int(systolic):
                raise forms.ValidationError(_("Distolic may not exceed Systolic."))
        return cleaned_data


    def clean_systolic(self):
        systolic     = self.cleaned_data.get("systolic", "")
        if systolic:
            if not 80 <= int(systolic) <= 220:
                raise forms.ValidationError(_("Systolic pressure must be between 80 and 220."))
        return systolic
    
    def clean_diastolic(self):
        diastolic  = self.cleaned_data.get("diastolic", "")
        if diastolic:
            if not 40 <= int(diastolic) <= 130:
                raise forms.ValidationError(_("Distolic pressure must be between 40 and 130."))
        return diastolic
        

class ArchimedesCholesterolForm(ModelForm):
    class Meta:
        model = ArchimedesRiskAssessment
        fields = ('cholesterol', 'hdl', 'ldl',)
    required_css_class = 'required'
    
    
    def clean(self):
        cleaned_data = super(ArchimedesCholesterolForm, self).clean()
        hdl           = cleaned_data.get("hdl", "")
        ldl           = cleaned_data.get("ldl", "")
        cholesterol   = cleaned_data.get("cholesterol", "")
    
        if cholesterol:
            combined = int(hdl) + int(ldl)
        
            if combined > int(cholesterol):
                raise forms.ValidationError(_("Total cholesterol cannot exceed the sum of HDL + LDL cholesterol."))
        return cleaned_data

    def clean_cholesterol(self):
        cholesterol = self.cleaned_data.get("cholesterol", "")
        if not 70 <= int(cholesterol) <= 500:    
            raise forms.ValidationError(_("Total cholesterol must be between 70 and 500."))
        return cholesterol

class ArchimedesMoreForm(ModelForm):
    
    class Meta:
        model = ArchimedesRiskAssessment
        fields = ('cholesterolmeds', 'aspirin', 'familymihistory', 'bloodpressuremedcount',         
                  'moderateexercise', 'vigorousexercise',
                  )
    required_css_class = 'required'


class ArchimedesDiabetesForm(ModelForm):
    
    class Meta:
        model = ArchimedesRiskAssessment
        fields = ('hba1c',)
    required_css_class = 'required'

    def clean_hba1c(self):
        hba1c     = self.cleaned_data.get("hba1c", "")

        if hba1c:
            if not 2 <= float(hba1c) <= 16:
                raise forms.ValidationError(_("HbA1c must be between 2 and 16."))
        return hba1c 



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
