#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.contrib.localflavor.us.us_states import US_STATES
import datetime

from django.forms import Form
from django import forms

from models import *
import datetime
from utils import *

from django.utils.translation import ugettext_lazy as _


class FindPharmacyForm(Form):
    address = forms.CharField(max_length=30, label=_("Address"),
                              initial="920 2ND AVENUE S.")
    city  = forms.CharField(max_length=60, label=_("City"),
                            initial="MINNEAPOLIS")
    state = forms.TypedChoiceField(choices=US_STATES, label=_("State"),
                                   initial="MN")
    zip   = forms.CharField(max_length=60, label=_("Zip"), required=False)
    required_css_class = 'required'


    def save(self):
      
        address = self.cleaned_data.get('address', "")
        city = self.cleaned_data.get('city', "")
        state = self.cleaned_data.get('state', "")
        zip = self.cleaned_data.get('state', "")
        
        geocode_addr_str = "%s+%s+%s" % (address, city, state)
        geocode_addr_str=geocode_addr_str.replace(" ", "+")         
        result = GoogleGeoCode(geocode_addr_str)
        sresult = SureScriptsPharmacy(result)
        
        result = {'googlejson': result, 'surescriptsjson': sresult}
        
        
        return result
        