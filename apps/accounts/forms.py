#!/usr/bin/env python
from django import forms
from  models import *
#from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.conf import settings
from django.core.mail import mail_admins
from ..locsetup.models import LocationSetup


class PasswordResetRequestForm(forms.Form):
    email= forms.CharField(max_length=75, label="Email")

class PasswordResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password*")
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password (again)*")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        if len(password1) < settings.MIN_PASSWORD_LEN:
            msg="Password must be at least %s characters long.  Be tricky!" % (settings.MIN_PASSWORD_LEN)
            raise forms.ValidationError(msg)
        return password2


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password")
    smscode  = forms.CharField(widget=forms.PasswordInput, max_length=5, label="SMS Code")

class SMSCodeForm(forms.Form):
    username= forms.CharField(max_length=30, label="Username")

    
    
class SignupForm(forms.Form):
    username = forms.CharField(max_length=30, label="Username")
    email = forms.EmailField(max_length=75, label="Email")
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=60, label="Last Name")
    organization = forms.CharField(max_length=100, label="Organization")
    worker_id = forms.CharField(max_length=4, label="Worker ID (A 4 digit number)")
    mobile_phone_number = USPhoneNumberField(max_length=15, label="Mobile Phone Number")
   
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=30,
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=30,
                                label="Password (again)")
    

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        if len(password1) < settings.MIN_PASSWORD_LEN:
            msg="Password must be at least %s characters long.  Be tricky!" % (settings.MIN_PASSWORD_LEN)
            raise forms.ValidationError(msg)
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'This email address is already registered.')
        
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).count()>0:
            raise forms.ValidationError(u'This username is already taken.')
        return username


    def save(self, profile_callback=None):
        new_user = User.objects.create_user(
                        username=self.cleaned_data['username'],
                        password=self.cleaned_data['password1'],
                        email=self.cleaned_data['email'])
        new_user.first_name = self.cleaned_data.get('first_name', "")
        new_user.last_name = self.cleaned_data.get('last_name', "")
        new_user.is_active = False
        new_user.save()
        location =LocationSetup.objects.get(pk=1)
        up=UserProfile.objects.create(
            user=new_user,
            location=location,
            organization=self.cleaned_data.get('organization', ""),
            mobile_phone_number=self.cleaned_data.get('mobile_phone_number', ""),
            worker_id = self.cleaned_data.get('worker_id', ""),
            )
        mail_msg ="""User %s %s (%s) from %s just requested an account.
        You must activate the users account and set permissions via the admin.
        """ % (new_user.first_name, new_user.last_name, new_user.email,
               up.organization)
        
        mail_admins("[HIVE]:A new user just registered and requires adjudication and activation",
                    mail_msg)
        
        
        return new_user
    
