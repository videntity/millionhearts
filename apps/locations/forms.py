from django.forms import ModelForm
from django import forms
from models import LocationSetup
from django.contrib.localflavor.us.forms import USStateField, USZipCodeField
from django.contrib.localflavor.us.us_states import US_STATES
from models import WARD_CHOICES



class LocationSetupForm(ModelForm):
    class Meta:
        model = LocationSetup
    zip=USZipCodeField()
    state=forms.TypedChoiceField(choices=US_STATES, initial="DC")
    ward=forms.TypedChoiceField(choices=WARD_CHOICES)
    required_css_class = 'required'