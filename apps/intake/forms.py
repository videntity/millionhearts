#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.forms import ModelForm
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from models import PatientProfile, Locator, Visit, YES_NO_CHOICES, GENDER_CHOICES
import datetime
from django.contrib.localflavor.us.forms import USStateField, USZipCodeField
from django.contrib.localflavor.us.us_states import US_STATES
from ..widgets import ClientSignatureWidget, WorkerSignatureWidget
from utils import create_patient_id

#init a few things about dates
def dob_range():
    this_year = datetime.date.today().year
    years = range(this_year-80, this_year-10)
    return years


#init a few things about dates
def last_doc_range():
    this_year = datetime.date.today().year
    years = range(this_year-10, this_year+1)
    return years


class PatientSearchForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name  = forms.CharField(required=False)

class Last4SocialSearchForm(forms.Form):
    last_4_ssn = forms.CharField(max_length=4)

    def clean_last_4_ssn(self):
        last_4_ssn=self.cleaned_data.get("last_4_ssn", "")
        if len(str(last_4_ssn))!=4:
             raise forms.ValidationError("You must supply exactly 4 digits.")
        
        
        return last_4_ssn

class LocatorForm(ModelForm):
    class Meta:
        model = Locator
        exclude = ('patient','worker', 'locator', 'grant', 'thumbnail')
    creation_date=forms.DateField(initial=datetime.date.today,
                                  widget=SelectDateWidget(),
                                  label="Creation Date")
    patient_signature=forms.CharField(widget=ClientSignatureWidget())
    worker_signature=forms.CharField(widget=WorkerSignatureWidget())
    required_css_class = 'required'



class QuickIntakeForm(ModelForm):
    class Meta:
        model = PatientProfile
        fields = ('first_name', 'last_name', 'gender','last_4_ssn','reciept_privacy_practices')
    gender = forms.TypedChoiceField(initial = None, required=True, choices = GENDER_CHOICES)
    reciept_privacy_practices = forms.TypedChoiceField(initial = False, choices =YES_NO_CHOICES,
                    label="The client signed and received a copy of Notice of Privacy Practices")
    patient_signature=forms.CharField(widget=ClientSignatureWidget())
    required_css_class = 'required'
    
    def clean_reciept_privacy_practices(self):
        reciept_privacy_practices = self.cleaned_data.get("reciept_privacy_practices", "")
        if reciept_privacy_practices == "False" or reciept_privacy_practices == False or reciept_privacy_practices == "":
            raise forms.ValidationError("You must provide the client with a copy of privacy practices and answer Yes to this question.")
        return reciept_privacy_practices
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "")
        if not first_name.isalpha():
            raise forms.ValidationError("First Name must be all letters. No numbers, whitespaces, etc.")
        
        if len(first_name) < 2:
            raise forms.ValidationError("First Name must be at least 2 letters")
        
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", "")
        if not last_name.isalpha():
            raise forms.ValidationError("Last Name must be all letters. No numbers, whitespaces, etc.")
        
        if len(last_name) < 2:
            raise forms.ValidationError("Last Name must be at least 2 letters")
        
        return last_name
    
    def clean_last_4_ssn(self):
        last_4_ssn = self.cleaned_data.get("last_4_ssn", "")
        first_name = self.cleaned_data.get("first_name", "")
        last_name = self.cleaned_data.get("last_name", "")
                
        try:
            int(last_4_ssn)
        except:
            raise forms.ValidationError("You must supply exactly 4 digits.")          
        
        if len(str(last_4_ssn))!=4:
             raise forms.ValidationError("You must supply exactly 4 digits.")
             
        pat_id = create_patient_id(first_name, last_name, last_4_ssn)
    
        try:
            p=PatientProfile.objects.get(patient_id=pat_id)
            raise forms.ValidationError("This user already exists. Try searching instead of an intake.")
        except(PatientProfile.DoesNotExist):
            pass
        return last_4_ssn




class QuickReferralIntakeForm(ModelForm):
    class Meta:
        model = PatientProfile
        fields = ('first_name', 'last_name', 'gender','last_4_ssn')
    
    gender = forms.TypedChoiceField(initial = None, required=True, choices = GENDER_CHOICES)
    required_css_class = 'required'
    
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "")
        if not first_name.isalpha():
            raise forms.ValidationError("First Name must be all letters. No numbers, whitespaces, etc.")
        if len(first_name) < 2:
            raise forms.ValidationError("First Name must be at least 2 letters")
        
        
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", "")
        if not last_name.isalpha():
            raise forms.ValidationError("Last Name must be all letters. No numbers, whitespaces, etc.")
        if len(last_name) < 2:
            raise forms.ValidationError("Last Name must be at least 2 letters")
        
        return last_name
    
    def clean_last_4_ssn(self):
        last_4_ssn = self.cleaned_data.get("last_4_ssn", "")
        first_name = self.cleaned_data.get("first_name", "")
        last_name = self.cleaned_data.get("last_name", "")
                
        try:
            int(last_4_ssn)
        except:
            raise forms.ValidationError("You must supply exactly 4 digits.")          
        
        if len(str(last_4_ssn))!=4:
             raise forms.ValidationError("You must supply exactly 4 digits.")
             
        pat_id = create_patient_id(first_name, last_name, last_4_ssn)
    
        try:
            p=PatientProfile.objects.get(patient_id=pat_id)
            raise forms.ValidationError("This user already exists. Try searching instead of an intake.")
        except(PatientProfile.DoesNotExist):
            pass
        return last_4_ssn





class IntakeForm(ModelForm):
    class Meta:
        model = PatientProfile
        fields = (
                 #'grants', #uncomment to allow tester to assign grants upon intake
                  'redeem_coupon','first_name','last_name', 'nick_name','last_4_ssn','address1',
                   'address2', 'city', 'state', 'zip', 'county', 'ward', 'gender',
                   'has_medical_home', 'medical_home_last_visit',                  
                   'chief_complaint', 'medical_history_heart_disease',
                   'medical_history_hypertension', 'medical_history_alzheimers',
                   'medical_history_diabetes', 'medical_history_asthma', 'height_inches',
                   'veteran_status','race_no_answer','race_black', 'race_white',
                   'race_american_indian','race_native_hawaiian_or_pac_islander',
                   'race_asian', 'race_alaskan_native', 'race_other',
                   'ethnicity', 'health_insurance_provider',
                   'date_of_birth',
                   'home_phone_number',
                   'mobile_phone_number', 'email', 'reciept_privacy_practices',
                   )
    date_of_birth = forms.DateField(widget = SelectDateWidget(years=dob_range()),
                                    label = "Date of Birth", required=False)
    medical_home_last_visit = forms.DateField(widget=SelectDateWidget(
                                    years = last_doc_range()), required=False,
                                    label = "Approximately when was the last time you saw your primary care doctor?")

    state = forms.TypedChoiceField(initial = 'DC', choices =US_STATES, 
                                label="State")

    city = forms.CharField(initial = 'Washington', label="City")
    reciept_privacy_practices = forms.TypedChoiceField(initial = False, choices =YES_NO_CHOICES,
                                label="The patient signed and received a copy of Notice of Privacy Practices")
    
    patient_signature=forms.CharField(widget=ClientSignatureWidget())

    required_css_class = 'required'
    
    def clean_reciept_privacy_practices(self):
        reciept_privacy_practices = self.cleaned_data.get("reciept_privacy_practices", "")
        if reciept_privacy_practices == "False" or \
            reciept_privacy_practices == False or \
            reciept_privacy_practices == "":
            raise forms.ValidationError("You must provide the client with a copy of privacy practices and answer Yes to this question.")
        return reciept_privacy_practices
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "")
        if not first_name.isalpha():
            raise forms.ValidationError("First Name must be all letters. No numbers, whitespaces, etc.")
        if len(first_name) < 2:
            raise forms.ValidationError("First Name must be at least 2 letters")        
        
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", "")
        if not last_name.isalpha():
            raise forms.ValidationError("Last Name must be all letters. No numbers, whitespaces, etc.")
        if len(last_name) < 2:
            raise forms.ValidationError("Last Name must be at least 2 letters")
        
        return last_name
    
    def clean_last_4_ssn(self):
        last_4_ssn = self.cleaned_data.get("last_4_ssn", "")
        first_name = self.cleaned_data.get("first_name", "")
        last_name = self.cleaned_data.get("last_name", "")
                
        try:
            int(last_4_ssn)
        except:
            raise forms.ValidationError("You must supply exactly 4 digits.")          
        
        if len(str(last_4_ssn))!=4:
             raise forms.ValidationError("You must supply exactly 4 digits.")
             
        pat_id = create_patient_id(first_name, last_name, last_4_ssn)
    
        try:
            p=PatientProfile.objects.get(patient_id=pat_id)
            raise forms.ValidationError("This user already exists. Try searching instead of an intake.")
        except(PatientProfile.DoesNotExist):
            pass
        return last_4_ssn
        
    

class EditIntakeForm(ModelForm):
    class Meta:
        model = PatientProfile
        fields = (
                   'first_name','last_name', 'last_4_ssn',
                   'nick_name','address1',
                   'gender', 'address2', 'city', 'state', 'zip', 'county', 'ward',
                   'date_of_birth', 'veteran_status', 'health_insurance_provider',
                   'home_phone_number', 'mobile_phone_number', 'has_medical_home',
                   'medical_home_last_visit', 'chief_complaint',
                   'medical_history_heart_disease', 'medical_history_hypertension',
                   'medical_history_alzheimers', 'medical_history_diabetes',
                   'medical_history_asthma', 'email', 'height_inches',
                   'veteran_status','race_no_answer','race_black', 'race_white',
                   'race_american_indian','race_native_hawaiian_or_pac_islander',
                   'race_asian', 'race_alaskan_native', 'race_other',
                   'ethnicity',
                   )
    date_of_birth = forms.DateField(widget = SelectDateWidget(years=dob_range()),
                                    label = "Date of Birth", required=False)
    
    state = forms.TypedChoiceField(initial = 'DC', choices =US_STATES, 
                                label="State")
    medical_home_last_visit = forms.DateField(widget=SelectDateWidget(
                                    years = last_doc_range()), required=False,
                                    label = "Approximately when was the last time you saw your primary care doctor?")

    city = forms.CharField(initial = 'Washington', label="City")
    zip = USZipCodeField()
    state = forms.TypedChoiceField(choices=US_STATES, initial="DC")
    required_css_class = 'required'
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "")
        if not first_name.isalpha():
            raise forms.ValidationError("First Name must be all letters. No numbers, whitespaces, etc.")
        if len(first_name) < 2:
            raise forms.ValidationError("First Name must be at least 2 letters")        
        
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", "")
        if not last_name.isalpha():
            raise forms.ValidationError("Last Name must be all letters. No numbers, whitespaces, etc.")
        if len(last_name) < 2:
            raise forms.ValidationError("Last Name must be at least 2 letters")
        
        return last_name
    
    def clean_last_4_ssn(self):
        last_4_ssn = self.cleaned_data.get("last_4_ssn", "")
        first_name = self.cleaned_data.get("first_name", "")
        last_name = self.cleaned_data.get("last_name", "")
                
        try:
            int(last_4_ssn)
        except:
            raise forms.ValidationError("You must supply exactly 4 digits.")          
        
        if len(str(last_4_ssn))!=4:
             raise forms.ValidationError("You must supply exactly 4 digits.")
             
        return last_4_ssn
        

    
class EditOverviewForm(ModelForm):
    class Meta:
        model = PatientProfile
        fields = ('chief_complaint','reason_for_visit', 'next_steps',)
    required_css_class = 'required'


class MarkVisitForm(ModelForm):
    class Meta:
        model = Visit
        exclude = ('worker', 'patient')
    required_css_class = 'required'

