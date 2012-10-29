#!/usr/bin/env python
from django import forms
from  models import *
#from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.conf import settings
from django.core.mail import mail_admins
from django.utils.translation import ugettext_lazy as _

class PasswordResetRequestForm(forms.Form):
    email= forms.CharField(max_length=75, label=_("Email"))
    required_css_class = 'required'
    
class PasswordResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=30,
                                label=_("Password*"))
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=30,
                                label=_("Password (again)*"))

    required_css_class = 'required'
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        if len(password1) < settings.MIN_PASSWORD_LEN:
            msg=_("Password must be at least %s characters long. Be tricky!") % (settings.MIN_PASSWORD_LEN)
            raise forms.ValidationError(msg)
        return password2


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label=_("Username"))
    password = forms.CharField(widget=forms.PasswordInput, max_length=30,
                               label=_("Password"))

    required_css_class = 'required'
    
class SignupForm(forms.Form):
    username = forms.CharField(max_length=30, label=_("Username"))
    

    mobile_phone_number = USPhoneNumberField(max_length=15,
                                             label=_("Mobile Phone Number"),
                                             required=False)
    preferred_contact_method = forms.TypedChoiceField(
                label =_("Preferred Contact Method"),
                choices = CONTACT_CHOICES)
    email = forms.EmailField(max_length=75, label=_("Email"), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=30,
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=30,
                                label=_("Password (again)"))
    
    required_css_class = 'required'
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        if len(password1) < settings.MIN_PASSWORD_LEN:
            msg=_("Password must be at least %s characters long.  Be tricky!") % (settings.MIN_PASSWORD_LEN)
            raise forms.ValidationError(msg)
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email', "")
        if email:
            username = self.cleaned_data.get('username')
            if email and User.objects.filter(email=email).exclude(username=username).count():
                raise forms.ValidationError(_('This email address is already registered.'))
            return email
        else:
            return "foo@bar.com"

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).count()>0:
            raise forms.ValidationError(_('This username is already taken.'))
        return username


    def save(self, patient_id, language_code):
        new_user = User.objects.create_user(
                        username=self.cleaned_data['username'],
                        password=self.cleaned_data['password1'],
                        email=self.cleaned_data['email'])
        new_user.save()
        
        up=UserProfile.objects.create(
            user=new_user,
            patient_id = patient_id,
            preferred_contact_method=self.cleaned_data.get('preferred_contact_method', ""),
            preferred_language=language_code,
            mobile_phone_number=self.cleaned_data.get('mobile_phone_number', ""),
            ) 
        return new_user
    
class AccountSettingsForm(forms.Form):

    username = forms.CharField(max_length=30, label=_("Username"))
    preferred_contact_method = forms.TypedChoiceField(
                                label =_("How do you prefer to be contacted for a follow up?"),
                                choices = CONTACT_CHOICES,)
    mobile_phone_number = USPhoneNumberField(max_length=12,
                    label=_("Mobile Phone Number"),
                    required=False)    
    email = forms.CharField(max_length=30, label=_("Email"), required=False)

    
    required_css_class = 'required'
    
    def clean_twitter(self):
        twitter = self.cleaned_data.get("twitter", "")
        if twitter!="":
            if twitter[0:1]=="@":
                twitter=twitter[1:]
        return twitter
    
    def clean_email(self):
        email = self.cleaned_data.get('email', "")
        if email:
            username = self.cleaned_data.get('username')
            if email and User.objects.filter(email=email).exclude(email=email).count():
                raise forms.ValidationError(_('This email address is already registered.'))   
            return email
        else:
            return "foo@bar.com"

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exclude(username=username).count():
            raise forms.ValidationError(_('This username is already taken.'))
        return username
