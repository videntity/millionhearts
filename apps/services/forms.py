#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.forms import ModelForm
from django import forms
from models import *
from django.forms.extras.widgets import SelectDateWidget
import datetime
from django.contrib.localflavor.us.forms import USStateField, USZipCodeField
from django.contrib.localflavor.us.us_states import US_STATES
from ..organizations.models import Service



this_year = datetime.date.today().year
years = range(this_year-80, this_year-10)
this_year_only= range(this_year, this_year+1)

class ReferralForm(ModelForm):
    class Meta:
        model = Referral
        exclude = ('patient','worker', 'cpt_code', 'icd9_code', 'icd10_code')
    creation_date=forms.DateField(initial=datetime.date.today,
                                  widget=SelectDateWidget())

    required_css_class = 'required'
    
    def clean_organization(self):
        organization = self.cleaned_data["organization"]
        referral_type = self.cleaned_data["referral_type"]
        
        service_slugs = []
        services = organization.services.all()
        for s in services:
            service_slugs.append(s.slug)
        #if the referral_type is not something the service provides, then Val Er.
        if not referral_type in service_slugs:
            msg ="%s does not provide %s." % (organization, referral_type)
            raise forms.ValidationError(msg)
        
        return organization
    


class SelectReferralTypeForm(ModelForm):
    class Meta:
        model = Linkage
        fields = ('referral_type',)
    
class LinkageForm2(ModelForm):
    class Meta:
        model = Linkage
        exclude = ('patient','worker', 'cpt_code', 'icd9_code', 'icd10_code',
                   'cpt_modifier_codes', 'personnel_expense')
    creation_date=forms.DateField(initial=datetime.date.today,
                                  widget=SelectDateWidget())
    linkage_date=forms.DateField(initial=datetime.date.today,
                                  widget=SelectDateWidget())
    required_css_class = 'required'
    
    def __init__(self,referral_type_slug,*args,**kwargs):
        super (LinkageForm2,self ).__init__(*args,**kwargs) # populates the post
        s = Service.objects.filter(slug=referral_type_slug)
        self.fields['referral_type'].initial = referral_type_slug
        self.fields['organization'].queryset = Organization.objects.filter(
                                                        services=s)


    
class LinkageForm(ModelForm):
    class Meta:
        model = Linkage
        exclude = ('patient','worker', 'cpt_code', 'icd9_code', 'icd10_code',
                   'cpt_modifier_codes ', 'personnel_expense')
    creation_date=forms.DateField(initial=datetime.date.today,
                                  widget=SelectDateWidget())
    linkage_date=forms.DateField(initial=datetime.date.today,
                                  widget=SelectDateWidget())
    required_css_class = 'required'
    
    def clean_organization(self):
        organization = self.cleaned_data["organization"]
        referral_type = self.cleaned_data["referral_type"]
        
        service_slugs = []
        services = organization.services.all()
        for s in services:
            service_slugs.append(s.slug)
        #if the referral_type is not something the service provides, then Val Er.
        if not referral_type in service_slugs:
            msg ="%s does not provide %s." % (organization, referral_type)
            raise forms.ValidationError(msg)
        
        return organization
    
class LinkageFollowUpForm(ModelForm):
    class Meta:
        model = LinkageFollowUp
        exclude = ('linkage','worker', 'cpt_code', 'icd9_code', 'icd10_code',
                   'cpt_modifier_codes', 'personnel_expense')
    required_css_class = 'required'
    creation_date=forms.DateField(initial=datetime.date.today,
                                  widget=SelectDateWidget())
 


