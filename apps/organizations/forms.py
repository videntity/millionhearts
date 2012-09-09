#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django import forms
from models import *

ORG_TYPE_CHOICES =( ('ANY',                 'Any'),
                    ('FREE-CLINIC',         'Free Clinic'),
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


class OrganizationSearchForm(forms.Form):
    name = forms.CharField(required=False)
    organization_type = forms.ChoiceField(label = "Organization Type",
                                          choices=ORG_TYPE_CHOICES,
                                          required=False,
                                          initial="ANY")



class ProviderSearchForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name  = forms.CharField(required=False)


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
    required_css_class = 'required'


class PatientCareTeamForm(forms.ModelForm):
    class Meta:
        model = PatientCareTeam
        exclude = ('creation_date',)
    required_css_class = 'required'


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
    required_css_class = 'required'