#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import datetime

from datetime import timedelta, date

from sorl.thumbnail import ImageField

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.localflavor.us.us_states import US_STATES
from django.contrib.localflavor.us.models import PhoneNumberField

from ..locations.models import LocationSetup


from utils import create_patient_id, update_filename, create_anonymous_patient_id


SURVEY_STATUS = (('incomplete','Incomplete'),
                 ('error','In error'),
                 ('complete','Complete'),)

WARD_CHOICES = (('1','1'), ('2','2'), ('3','3'),
                ('4','4'), ('5','5'), ('6','6'),
                ('7','7'), ('8','8'), ('9','9'))

GENDER_CHOICES = (('MALE', 'MALE'), 
                 ('FEMALE', 'FEMALE'),
                 ('TRANSGENDER-MALE-TO-FEMALE', 'TRANSGENDER-MALE-TO-FEMALE'),
                 ('TRANSGENDER-FEMALE-TO-MALE', 'TRANSGENDER-FEMALE-TO-MALE'))

HEALTH_PROVIDER_CHOICES = (('NONE', 'NONE'), 
                           ('SELF', 'SELF'),
                           ('PUBLIC-ASSIST', 'PUBLIC-ASSIST'),  
                           ('MILITARY/VA', 'MILITARY/VA'),
                           ('EMPLOYER', 'EMPLOYER'), 
                           ('UNKNOWN', 'UNKNOWN'))

ETHNICITY_CHOICES = (('0', 'NON-HISPANIC'), ('1', 'HISPANIC'))

YES_NO_CHOICES = ((True,'Yes'), (False, 'No'))


class Visit(models.Model):

    patient       = models.ForeignKey('PatientProfile')
    worker       = models.ForeignKey(User)
    creation_date = models.DateField(default=date.today)
    
    def __unicode__(self):
        return '%s processed on %s' % (self.patient.patient_id, self.creation_date)
    
    class Meta:
        unique_together = (("patient", "creation_date"),)
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)

        
def last_seen(pid):
    v=Visit.objects.filter(patient__patient_id=pid)
    if len(v) == 1:
        return v[0].creation_date 
    elif len(v) == 0:
        return None
    elif len(v) > 0:
        return v[1].creation_date
    else:
        return None


def seen_in_past_year(pid):
    try:
        v = Visit.objects.filter(patient__patient_id=pid).exclude(creation_date=date.today()).latest()
        #check an see if we have seen this person in the past year.
        today = date.today()
        oneyearago = today - timedelta(days=356)
        if oneyearago < v.creation_date:
            return True
        else:
            return False
    except(Visit.DoesNotExist):
        return False
    
    
def seen_before(pid):
    try:
        v = Visit.objects.filter(patient__patient_id=pid).reverse().latest()
        v_result = True
        # print v.creation_date, date.today()
        if v.creation_date != date.today():
            v_result = True
            return v_result

        v_result = False
        return v_result
    except:
        v_result = False
        return v_result
    
    
# todo: this should be part of the model
def number_of_prior_visits(pid):
    v = 0
    v = v + Visit.objects.filter(patient__patient_id=pid)\
    .exclude(creation_date=date.today()).count()
    return v

class PatientProfile(models.Model):
    
    patient_id = models.CharField(max_length=10, blank=True, unique=True,
                                  verbose_name=u'Patient ID')
    photo = ImageField(upload_to=update_filename,
                       default="", blank=True)
    anonymous_patient_id = models.CharField(max_length=16,       
                                  unique=True,
                                  verbose_name=u'Anonymous Patient ID',
                                  default=create_anonymous_patient_id,
                                  #editable=False
                                  )
 
    is_recruiter = models.BooleanField(default=False)

    redeem_coupon = models.CharField(max_length=5, default="", blank=True,
                                     null=True,
                                    verbose_name="Coupon #")

    visit_count = models.IntegerField(max_length=4,  default=0)
    worker      = models.ForeignKey(User)
    location    = models.ForeignKey(LocationSetup)

    first_name = models.CharField(max_length=50,verbose_name='First Name')
    last_name = models.CharField(max_length=50, verbose_name='Last Name')
    nick_name = models.CharField(max_length=50, verbose_name='Nick Name', 
                                 blank=True, null=True)

    last_4_ssn = models.CharField(max_length=4,
                                  verbose_name='Last 4 Digits of SSN')

    chief_complaint = models.TextField(max_length=2048, blank=True, default="",
                        verbose_name ="Do you have an untreated medical condition you would like to tell us about?")
    
    health_insurance_provider = models.CharField(max_length=20, blank=True, default="",
                                    verbose_name='Who is your health insurance provider?',
                                    choices=HEALTH_PROVIDER_CHOICES)
    
    has_medical_home = models.BooleanField(default=False, choices =YES_NO_CHOICES,
                                        verbose_name="Do you have a primary care doctor?")

    medical_home_last_visit = models.DateField(blank=True, null=True, 
                                verbose_name="Approximately when was the last time you saw your primary care doctor?")


    medical_history_heart_disease = models.BooleanField(blank=True,  choices =YES_NO_CHOICES,
                                verbose_name="Personal/Family History of Cardiovascular (Heart) Disease?")

    medical_history_hypertension = models.BooleanField(blank=True,  choices =YES_NO_CHOICES,
                                verbose_name="Personal/Family History of High Blood Pressure/Hypertension?")

    medical_history_alzheimers = models.BooleanField(blank=True,  choices =YES_NO_CHOICES,
                                verbose_name="Personal/Family History of Alzheimer's?")

    medical_history_diabetes = models.BooleanField(blank=True,  choices =YES_NO_CHOICES,
                                verbose_name="Personal/Family History of Diabetes?")

    medical_history_asthma = models.BooleanField(blank=True,  choices =YES_NO_CHOICES,
                                verbose_name="Personal/Family History of Asthma?")

    
    email = models.EmailField(max_length=100, blank=True, default="",
                                           verbose_name='Email')
    
    mobile_phone_number = PhoneNumberField(max_length=15, blank=True, default="",
                                           verbose_name='Mobile Phone #')

    home_phone_number = PhoneNumberField(max_length=15, blank=True, default="",
                                        verbose_name='Home Phone #')

    height_inches = models.CharField(max_length=3, verbose_name='Height in Inches',
                                       blank=True, default="")
    address1 = models.CharField(max_length=100, blank=True, default="", verbose_name='Address')
    address2 = models.CharField(max_length=100, blank=True, default="",
                                verbose_name='Address Line 2' )

    city = models.CharField(max_length=100, verbose_name='City',
                            default="", blank=True)
    zip = models.CharField(max_length=10, verbose_name='Zip Code',
                           default="", blank=True)
    state = models.CharField(blank=True, max_length=2, choices=US_STATES,
                             verbose_name='State')

    county = models.CharField(blank=True, default="", max_length=75,
                              verbose_name='County')

  
    date_of_birth = models.DateField(blank=True, null=True,
                                     verbose_name="Date of Birth")
    
    gender = models.CharField(max_length=30,
                              verbose_name='Gender',
                              choices=GENDER_CHOICES,
                              blank=True)

    veteran_status = models.BooleanField(max_length=1,
                              verbose_name='Are you a veteran?',
                              default=False, blank=True,
                              choices=((False,"No"),(True,"Yes")))
    
    abused_substances =  models.CharField(max_length=2,
                              verbose_name='Do you currently abuse or have ever abused substances?',
                              default="98",
                              choices=(("0","No"),("1","Yes"), ("98","Left Blank"),))
    
    substances_in_treatment = models.BooleanField(verbose_name='Are you in treatment for substance abuse?',
                              default=False,
                              choices=((False,"No"),(True,"Yes")))
    
    reason_for_visit     = models.TextField(max_length=2048, blank=True, default="",
                                verbose_name="Reason for Visit")
    
    next_steps          = models.TextField(max_length=2048, blank=True, default="",
                                verbose_name="Next Steps")
    
    
    substances_in_recovery  = models.BooleanField(max_length=1,
                              verbose_name='Are you in recovery for substance abuse?',
                              default=False, blank=True,
                              choices=((False,"No"),(True,"Yes")))

    race_no_answer = models.CharField(max_length=1, blank=True,
                                      verbose_name='Race: No Answer',
                                      default="0",
                                      choices=(("0","No"),("1","Yes")))
    
    race_black = models.CharField(max_length=1, blank=True,
                                  verbose_name='Race: Black',
                                  default="0",
                                  choices=(("0","No"),("1","Yes")))
    
    race_white = models.CharField(max_length=1,blank=True,
                                  verbose_name='Race: White',
                                  default="0",
                                  choices=(("0","No"),("1","Yes")))

    race_american_indian = models.CharField(max_length=1,blank=True,
                                            verbose_name='Race: American Indian',
                                            default="0",
                                            choices=(("0","No"),("1","Yes")))

    race_native_hawaiian_or_pac_islander = models.CharField(max_length=1,
                                                            blank=True,
                            verbose_name=('Race: Native Hawaiian or other Pacific Islander'),
                            default="0", choices=(("0","No"),("1","Yes")))
     
    race_asian = models.CharField(max_length=1, blank=True,
                                  verbose_name='Race: Asian',
                                  default="0",
                                  choices=(("0","No"),("1","Yes")))    

    race_alaskan_native = models.CharField(max_length=1, blank=True,
                                           verbose_name='Race: Alaskan Native',
                                           default="0",
                                           choices=(("0","No"),("1","Yes"))) 

    race_other =  models.CharField(max_length=1, blank=True,
                                   verbose_name='Race: Other',
                                   default="0",
                                   choices=(("0","No"),("1","Yes")))

    ethnicity = models.CharField(max_length=1, blank=True,
                                 verbose_name='Ethnicity',
                                 default="0",
                                 choices=ETHNICITY_CHOICES)
    
    reciept_privacy_practices = models.BooleanField(default = False,
                                    choices =YES_NO_CHOICES,
                                    verbose_name="The client signed and received a copy of Notice of Privacy Practices")
    
    
    
    cageaid_substance_abuse_screen_complete = models.BooleanField(default=False)
    ada_type2_diabetes_screen_complete = models.BooleanField(default=False)
    
    
    framingham10yr_test_complete = models.BooleanField(default=False)
    framingham10yr_grouped_consent_complete = models.BooleanField(default=False)
    
    cardio_diabetes_risks_complete = models.BooleanField(default=False)
    

    patient_signature   = models.TextField(max_length=25000, blank=True, default="")
    creation_date       = models.DateField(default=date.today, verbose_name="Creation Date")
    creation_dt         = models.DateTimeField(auto_now_add=True)
    update_dt           = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return '%s %s (%s)' % (self.first_name, self.last_name, self.patient_id)
        
    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
    
    def save(self, **kwargs):
        super(PatientProfile, self).save(**kwargs)
        
        if self.anonymous_patient_id=="":
            self.anonymous_patient_id=create_anonymous_patient_id()
        self.patient_id =create_patient_id(self.first_name,
                                            self.last_name,
                                            str(self.last_4_ssn))            

        self.last_modified_date = date.today()

        try:
            v = Visit.objects.get(patient=self,

                                    creation_date=self.creation_date)
        except Visit.DoesNotExist:
            Visit.objects.create(patient=self, worker=self.worker,
                                    creation_date=self.creation_date)
       
        
        if self.redeem_coupon != "":
            try:
                c=Coupon.objects.get(coupon_code=self.redeem_coupon)
                c.is_valid=False
                c.member_redeemed=self
                c.save()
            except(Coupon.DoesNotExist):    
                pass
        super(PatientProfile, self).save(**kwargs)        




#@receiver(post_save, sender=Locator)
#def my_handler(sender, **kwargs):
#    print kwargs['instance']
#    print "post_save"
#post_save.connect(my_handler, sender=Locator)

class Coupon(models.Model):  
    coupon_code         = models.CharField(max_length=5, blank=True, unique=True)
    worker              = models.ForeignKey(User, blank=True, null=True)
    name                = models.CharField(max_length=50, blank=True, default="")
    detail              = models.CharField(max_length=140, blank=True, default="")
    member_issued       = models.ForeignKey(PatientProfile,
                                        related_name="member_issued_coupon")
    member_redeemed     = models.ForeignKey(PatientProfile,
                                        blank=True, null=True,
                                        related_name="member_redeemed_coupon")
    
    is_valid            = models.BooleanField(default=True)
    issued              = models.DateField(default=date.today)
    expires             = models.DateField(default=date.today)
                           
    def __unicode__(self):
        return 'Code:%s | Issued to:%s | Redeemed by:%s |  Expires:%s | Is Valid:%s' % (
            self.coupon_code, self.member_issued, self.member_redeemed,
            self.expires, self.is_valid)
        
    def save(self, **kwargs):
        
        if not self.coupon_code:
            randcode=random.randint(1000,9999)
            self.coupon_code=str(randcode)
        today = date.today()
        self.expires=today + timedelta(days=settings.COUPON_EXPIRE_DAYS)
        self.name=settings.COUPON_NAME
        self.detail=settings.COUPON_DETAIL
        
        super(Coupon, self).save(**kwargs)
