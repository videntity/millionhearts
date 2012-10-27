#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=

import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from utils import ArchimedesAssessmentAPI 

from ..intake.models import PatientProfile
from ..accounts.models import UserProfile

from framingham10yr.framingham10yr import framingham_10year_risk

import json
from utils import create_anonymous_patient_id
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta

YN_CHOICES = (('1', 'Yes'), ('0', 'No'))
BOOL_CHOICES = ((True, "Yes"),(False, "No"))


GENDER_CHOICES = (('M', 'Male'), 
                 ('F', 'Female'),)

SMOKER_CHOICES = ((True, 'Yes'), 
                 (False, 'No'),)

YES_NO_CHOICES = ((True,'Yes'), (False, 'No'))

YES_NO_BINARY_CHOICES = (("yes",'Yes'), ("no", 'No'),)


class Framingham10yrHeartRiskTest(models.Model):
    patient                      = models.ForeignKey(PatientProfile)
    worker                       = models.ForeignKey(User)
    creation_date                = models.DateField(default=datetime.date.today)
    sex                          = models.CharField(choices=GENDER_CHOICES,
                                    max_length=6,
                                    verbose_name =_("What is your sex?"))
    age                          = models.IntegerField(max_length=3,
                                    verbose_name =_("What is your age?"))
    total_cholesterol            = models.IntegerField(max_length=3,
                                    verbose_name =_("What is your total choleterol?"))
    hdl_cholesterol              = models.IntegerField(max_length=3,
                                    verbose_name =_("What is your HDL cholesterol?"))
    systolic_blood_pressure      = models.IntegerField(max_length=3,
                                    verbose_name =_("What is your systolic blood pressure?"))
    smoker                       = models.BooleanField(choices = SMOKER_CHOICES,
                                    verbose_name =_("Do you smoke?"),
                                    help_text=_('Anser yes if you have smoked at all in the past 30 days'))
    blood_pressure_med_treatment = models.BooleanField(choices = YES_NO_CHOICES,
                                    verbose_name=_("Is the patient currently taking medication to lower blood pressure?"))
    points                       = models.IntegerField(default = 0,
                                                       blank = True,
                                                       max_length = 3 )
    percent_risk                 = models.CharField(default = "",
                                                    blank = True,
                                                    max_length = 5)


    def __unicode__(self):
        return '%s %s (%s)' % (self.patient.first_name, self.patient.last_name,
                               self.patient.patient_id)

    def save(self, **kwargs):
        self.patient.framingham10yr_test_complete = True
        self.patient.save()
        
        result = framingham10yr.framingham_10year_risk(self.sex, self.age,
                                        self.total_cholesterol,
                                        self.hdl_cholesterol,
                                        self.systolic_blood_pressure,
                                        self.smoker,
                                        self.blood_pressure_med_treatment)

        if result["status"] == 200:
            self.percent_risk = result["percent_risk"]   
            self.points = result["points"] 
            super(Framingham10yrHeartRiskTest, self).save(**kwargs)
        else:
            return result["errors"]

    class Meta:
        unique_together = (("patient", "creation_date"),)
        get_latest_by   = "creation_date"
        ordering        = ('-creation_date',)
        
        


RACE_CHOICES = (('BLACK', 'Black'), ('ASIAN', 'Asian'), ('WHITE', 'White'),
                ('NATIVE-AMERICAN','Native American'), )


ETHNICITY_CHOICES = (('NON-HISPANIC', 'Non-Hispanic'), ('HISPANIC', 'Hispanic'),  )

HEIGHT_CHOICES = ((44,"3' 8in" ),
    (45,"3' 9 in" ),
    (46,"3' 10 in" ),
    (47,"3' 11 in" ),
    (48,"4' 0 in" ),
    (49,"4' 1 in" ),
    (50,"4' 2 in" ),
    (51,"4' 3 in" ),
    (52,"4' 4 in" ),
    (53,"4' 5 in" ), 
    (54,"4' 6 in"),
    (55,"4' 7 in"),
    (56,"4' 8 in"),
    (57,"4' 9 in"),
    (58,"4' 10 in"),
    (59,"4' 11 in"),
    (60,"5' 0 in"),
    (61,"5' 1 in" ),
    (62,"5' 2 in" ),
    (63,"5' 3 in" ),
    (64,"5' 4 in" ),
    (65,"5' 5 in" ), 
    (66,"5' 6 in"),
    (67,"5' 7 in"),
    (68,"5' 8 in"),
    (69,"5' 9 in"),
    (70,"5' 10 in"),
    (71,"5' 11 in"),
    (72,"6' 0 in"),
    (73,"6' 1 in" ),
    (74,"6' 2 in" ),
    (75,"6' 3 in" ),
    (76,"6' 4 in" ),
    (77,"6' 5 in" ), 
    (78,"6' 6 in"),
    (79,"6' 7 in"),
    (80,"6' 8 in"),
    (81,"6' 9 in"),
    (82,"6' 10 in"),
    (84,"6' 11 in"),
    (85,"7' 0 in"),
    (86,"7' 1 in"),
    (87,"7' 2 in"),
    (88,"7' 3 in"),
    
    )

WEIGHT_CHOICES = zip(range(80, 601), range(80, 601))

AGE_CHOICES = zip(range(18, 131), range(18, 131))

BLOOD_PRES_MEDS_CHOICES = (("0","0"),("1","1"),("2","2"),("3","3"),("4","4"),)

def three_days_from_today():
    return datetime.date.today() + timedelta(days=4)

class ArchimedesRiskAssessment(models.Model):
    
    #Control fields
    patient_id       = models.CharField(max_length=20,
                            default=create_anonymous_patient_id)
    creation_date    = models.DateField(default=datetime.date.today)
    trackingid       = models.CharField(max_length=30, default="", blank=True)
        
    #Required assessment question fields ---------------------------------
    sex         = models.CharField(choices=GENDER_CHOICES, max_length=6,
                    verbose_name=_('Whats is your sex?'))
    age         = models.IntegerField(max_length=3, #choices = AGE_CHOICES,
                    verbose_name = _("What is your age?"))
    
    cholesterolmeds = models.CharField(choices=YES_NO_BINARY_CHOICES,
                        max_length=5,
                        verbose_name =_("Are you currently taking medication to control cholesterol?"))
    
    height      = models.IntegerField(max_length=3, choices = HEIGHT_CHOICES,
                    verbose_name = _("What is your height?"))
    weight      = models.IntegerField(max_length=3, #choices = WEIGHT_CHOICES,
                    verbose_name = _("What is your weight in pounds?"))
    smoker      = models.CharField(choices=YES_NO_BINARY_CHOICES, max_length=5,
                    #default="no",
                    verbose_name = _("Do you smoke?"),
                    help_text = _("Answer yes if you have smoked at all in the past 30 days."))
    
    #these are on the 2nd form ----------------------------------------------
    diabetes    = models.CharField(choices=YES_NO_BINARY_CHOICES,max_length=5,
                    default="no", 
                    verbose_name=_("Has a doctor ever told you that you have diabetes?"))
    stroke      = models.CharField(choices=YES_NO_BINARY_CHOICES,max_length=5,
                    default="no",
                    verbose_name=_("Has a doctor ever told you that you had a stroke?"))
    mi          = models.CharField(choices=YES_NO_BINARY_CHOICES, max_length=5,
                    default="no",
                    verbose_name=_("Has a doctor ever told you that you had a heart attack?"),
                    help_text = _("This is sometimes called a Myocardial Infarction or MI."))
    
    bloodpressuremeds = models.CharField(choices=YES_NO_BINARY_CHOICES,
                            max_length=5, default="no",
                            verbose_name =_("Are you currently taking medication to control your blood pressure?"))
    
    have_bp_chol_info = models.CharField(choices=YES_NO_BINARY_CHOICES, max_length=5,
                    default="no",
                    verbose_name=_("Do you have recent blood pressure and cholesterol numbers available?"),)
    
    #Optional Fields ---------------------------------------------------------
    systolic    = models.CharField(max_length=3,blank=True, default="",
                    verbose_name = _("What is your Systolic blood pressure (80-220) ?"))
    diastolic   = models.CharField(max_length=3,  blank=True, default="",
                    verbose_name = _("What is your Diastolic blood pressure (40-130) ?"))
        
    hdl         = models.CharField(max_length=3,blank=True, default="",
                    verbose_name = _("What is your HDL Cholesterol (20-130) ?"))
    ldl         = models.CharField(max_length=3, blank=True, default="",
                    verbose_name = _("What is your LDL Cholesterol (40 -400) ?"))    
    
    cholesterol = models.CharField(max_length=3,  blank=True, default="",
                    verbose_name = _("What is your Total Cholesterol (70-500) ?"))
    
    hba1c       = models.CharField(max_length=4, blank=True,
                    verbose_name = _("What is your HbA1c (2-16) ?"))

    bloodpressuremedcount = models.CharField(max_length=3, blank=True, default="0",
                                choices = BLOOD_PRES_MEDS_CHOICES,
                                verbose_name = _("If you answered yes to the previous question, how many blood pressure medications do you take each day?"))
    aspirin               = models.CharField(choices=YES_NO_BINARY_CHOICES,
                            max_length=5, default="no", blank=True,
                            verbose_name =_("Do you take aspirin regularly?"))
    moderateexercise      = models.CharField(max_length=3,  blank=True, default="",
                            verbose_name = _("How many hours of moderate exercise do you get per week (0-60)?"))
    vigorousexercise     = models.CharField(max_length=3,  blank=True, default="",
                            verbose_name = _("How many hours of vigorous exercise do you get per week (0-30)?"))
    familymihistory      = models.CharField(choices=YES_NO_BINARY_CHOICES, max_length=5,
                            default="", blank=True,
                            verbose_name=_("Has anyone in your immediate family had a hear attack before the age 55?"),
                            help_text = _("This is sometimes called a Myocardial Infarction or MI"))
    
    
    # status flags ------------------------------------------------------------
    basic_info_complete = models.BooleanField(default=True)
    
    blood_pressure_complete = models.BooleanField()

    cholesterol_complete = models.BooleanField()

    diabetes_complete = models.BooleanField()
    
    more_complete = models.BooleanField()

    signup_complete = models.BooleanField()
    
    follow_up_complete = models.BooleanField()
    
    origin  = models.CharField(max_length = 300, default="")
    
    destination = models.CharField(max_length = 300, default="")
    
    
    
    #Framingham risk
    framingham_risk  = models.CharField(max_length=20, blank=True, default="")    
    
    archimedes_json_result  = models.TextField(max_length=4096, default="",
                                                blank=True)
    
    #Follow Up -----------------------------------------------------------
    followup_date           = models.DateField(default=three_days_from_today)
    
    class Meta:
        unique_together = (("patient_id", "creation_date"),)
        get_latest_by   = "creation_date"
        ordering        = ('-creation_date',)

    def save(self, **kwargs):
        
        if not self.trackingid:
            self.trackingid = self.patient_id
            
        query={'gender'   : self.sex,
               'age'      : self.age,
               'height'   : self.height,         
               'weight'   : self.weight,
               'smoker'   : self.smoker,
               'diabetes' : self.diabetes, 
               'stroke'   : self.stroke,
               'mi'       : self.mi,
               'trackingid': self.trackingid,
               }

        if not self.signup_complete:
            try:
                up = UserProfile.objects.get(patient_id=self.patient_id)
                self.signup_complete = True
            except(UserProfile.DoesNotExist):
                pass
        
        #Add the optional values if they are populated
        if self.systolic:
            query['systolic'] = self.systolic

        if self.diastolic:
            query['diastolic'] = self.diastolic
        


        if self.systolic and self.diastolic:
             self.blood_pressure_complete = True


        if self.hdl:
            query['hdl'] = self.hdl
        
        if self.ldl:
            query['ldl'] = self.ldl
        

        if self.cholesterol:
            query['cholesterol'] = self.cholesterol
            
        if self.hdl and self.ldl and self.cholesterol:
             self.cholesterol_complete = True            

    
        if self.hba1c:
            query['hba1c'] = self.hba1c
            self.diabetes_complete = True  
        
        if self.cholesterolmeds:
            query['cholesterolmeds'] = self.cholesterolmeds
        
           
        if self.bloodpressuremeds:
            query['bloodpressuremeds'] = self.bloodpressuremeds

        if self.bloodpressuremedcount :
            query['bloodpressuremedcount '] = self.bloodpressuremedcount 


        if self.aspirin:
            query['aspirin'] = self.aspirin
            
        if self.moderateexercise:
            query['moderateexercise'] = self.moderateexercise
            
            
        if self.vigorousexercise:
            query['vigorousexercise'] = self.vigorousexercise
            
        if self.familymihistory:
            query['familymihistory'] = self.familymihistory
        
        if self.cholesterolmeds and self.bloodpressuremeds and \
           self.aspirin and self.bloodpressuremedcount and \
           self.moderateexercise and self.vigorousexercise and \
           self.familymihistory:
            self.more_complete = True
        
        result = ArchimedesAssessmentAPI(query)
        self.archimedes_json_result=result
    
    
        if  self.bloodpressuremeds and self.cholesterol and self.hdl  and \
            self.age and self.sex and  self.systolic and self.smoker:
            #print "calc framingham"
            fresult = framingham_10year_risk(self.sex,
                                         int(self.age),
                                        self.cholesterol,
                                        self.hdl,
                                        self.systolic,
                                        self.smoker,
                                        self.bloodpressuremeds
                                        )
            #print fresult
            if fresult.has_key("percent_risk"):
                self.framingham_risk = fresult["percent_risk"]
    
        super(ArchimedesRiskAssessment, self).save(**kwargs)
    

class CardioDiabetesRiskTest(models.Model):
    patient                      = models.ForeignKey(PatientProfile)
    worker                       = models.ForeignKey(User)
    creation_date                = models.DateField(default=datetime.date.today)
    race                         = models.CharField(choices=RACE_CHOICES,
                                                    max_length=20)
    ethnicity                    = models.CharField(choices=ETHNICITY_CHOICES,
                                                    max_length=20)
    medical_history_heart_disease = models.BooleanField(choices = YES_NO_CHOICES,
                                        verbose_name="Have you been diagnosed with cardiovascular (heart) disease?")
    physically_active	        = models.BooleanField(choices = YES_NO_CHOICES,
                                        verbose_name="Are you physically active?")
    medical_history_hypertension = models.BooleanField(choices = YES_NO_CHOICES,
                                        verbose_name="Have you been diagnosed with high blood pressure (hypertension)?")
    medical_history_diabetes	= models.BooleanField(choices = YES_NO_CHOICES,
                                        verbose_name="Have you been diagnosed with diabetes?")
    medical_history_alzheimers	= models.BooleanField(choices = YES_NO_CHOICES,
                                        verbose_name="Have you been diagnosed with Alzheimer's disease?")
    medical_history_asthma	= models.BooleanField(choices = YES_NO_CHOICES,
                                        verbose_name="Have you been diagnosed with asthma?")
    medical_history_sleep_apnea	= models.BooleanField(choices = YES_NO_CHOICES,
                                        verbose_name="Have you been diagnosed with sleep apnea?")
    medical_history_snor	= models.BooleanField(choices = YES_NO_CHOICES,
                                        verbose_name="Have you been told that you snor?")
    medical_history_kidney_disease = models.BooleanField(choices = YES_NO_CHOICES,
                                        verbose_name="Have you been diagnosed with kidney disease?")
    medical_history_high_cholesterol	= models.BooleanField(choices = YES_NO_CHOICES,
                                            verbose_name="Have you been diagnosed with high cholesterol?")
    medical_history_alcohol	= models.BooleanField(choices = YES_NO_CHOICES,
                                        verbose_name="Do you regularly have more than 2 alcoholic drinks per day?")
    medical_history_use_tobacco  = models.BooleanField(choices = YES_NO_CHOICES,
                                        verbose_name="Do you use tobacco?")
    family_history_diabetes	= models.BooleanField(choices = YES_NO_CHOICES,
                                        verbose_name="Do you have a father, brother, or sister with diabetes?")
    family_history_heart_disease = models.BooleanField(choices = YES_NO_CHOICES,
                                    verbose_name="Have either of your parents, your brothers, or your sisters been diagnosed with heart disease?")
    family_history_hypertension	= models.BooleanField(choices = YES_NO_CHOICES,
                                    verbose_name ="Have either of your parents or brothers or sisters been diagnosed with high blood pressure?")

    risk_list            = models.CharField(max_length=512)
    


    def __unicode__(self):
        return '%s %s (%s)' % (self.patient.first_name, self.patient.last_name,
                               self.patient.patient_id)

    def save(self, **kwargs):
        self.patient.cardio_diabetes_risks_complete = True
        self.patient.save()
        
        risks =[]
        
        if self.race != "WHITE":
            msg = "The %s race has a  predisposition for diabetes." % (self.race)
            risks.append(msg)
            
        if self.ethnicity == "HISPANIC":
            msg = "The %s ethnicity has predisposition for diabetes." % (self.ethnicity)
            risks.append(msg)   
        
        if self.medical_history_heart_disease:
            risks.append("You have a personal history of heart disease.")

        if self.medical_history_hypertension:
            risks.append("You have a personal history of hypertension.")                        
        
        if self.medical_history_diabetes:
            risks.append("You have a personal history of diabetes.")                    
                            
        if self.medical_history_asthma:
            risks.append("You have a personal history of asthma.")                    
        
        if self.medical_history_sleep_apnea:
            risks.append("You have a personal history of sleep apnea.")
                                
        if self.medical_history_snor:
            risks.append("You have a personal history of snoring.")
                                
        if self.medical_history_kidney_disease:
            risks.append("You have a personal history of kidney disease.")
                                
        if self.medical_history_high_cholesterol:
            risks.append("You have a personal history of high cholesterol.")
                                
        if self.medical_history_alcohol:
            risks.append("You have a personal history of drinking alcohol in excess.")
                                
        if self.medical_history_use_tobacco:
            risks.append("You have a personal history of tobacco use.")
                                
        if self.family_history_diabetes:
            risks.append("You have a family history of diabetes.")
                                
        if self.family_history_heart_disease:
            risks.append("You have a family history of heart disease.")
                                
        if self.family_history_hypertension:
            risks.append("You have a family history of hypertension.")
                                
        if not self.physically_active:
            risks.append("You have a personal history of a sedentary lifestyle.")

        number_of_risks = len(risks)
        msg = "You have %s risk factors for heart diesease and diabetes." % (number_of_risks)
        
        risks.insert(0, msg)
        self.risk_list = json.dumps(risks)
        
        super(CardioDiabetesRiskTest, self).save(**kwargs)


    class Meta:
        unique_together = (("patient", "creation_date"),)
        get_latest_by   = "creation_date"
        ordering        = ('-creation_date',)
        

CAGE_YES_NO_CHOICES = ((0,"No"),(1,"Yes"))     
        
class CAGEAIDSubstanceAbuseScreen(models.Model):
    patient             = models.ForeignKey(PatientProfile)
    worker              = models.ForeignKey(User)
    creation_date       = models.DateField(default=datetime.date.today)
    cage_1_cut_down     = models.IntegerField(max_length=1, choices=CAGE_YES_NO_CHOICES,
                            verbose_name ="Have you ever felt you ought to cut down on your drinking or drug use? ")
    cage_2_criticize    = models.IntegerField(max_length=1, choices=CAGE_YES_NO_CHOICES,
                            verbose_name ="Have people annoyed you by criticizing your drinking or drug use? ")
    cage_3_guilty       = models.IntegerField(max_length=1, choices=CAGE_YES_NO_CHOICES,
                            verbose_name ="Have you felt bad or guilty about your drinking or drug use?")
    cage_4_eye_opener   = models.IntegerField(max_length=1, choices=CAGE_YES_NO_CHOICES,
                            verbose_name ="Have you ever had a drink or used drugs first thing in the morning to steady your nerves or to get rid of a hangover (eye-opener)?")
    cage_score          = models.IntegerField(max_length=1, editable=False, verbose_name="Score")
    recommend_followup  = models.BooleanField(default=False, verbose_name="Recommend Followup",
                                              editable=False)
    
    
    class Meta:
        unique_together = (("patient", "creation_date"),)
        get_latest_by   = "creation_date"
        ordering        = ('-creation_date',)
        
        
    def save(self, **kwargs):
        self.patient.cageaid_substance_abuse_screen_complete = True
        self.patient.save()
        self.cage_score = self.cage_1_cut_down + self.cage_2_criticize + \
                          self.cage_3_guilty +  self.cage_4_eye_opener
     
        if self.cage_score >= 2:
            self.recommend_followup = True
        else:
            self.recommend_followup = False
        
        super(CAGEAIDSubstanceAbuseScreen, self).save(**kwargs)
        
DIABETES_RISK_1_CHOICES = ((0,"Less than 40 years"), (1, "40—49 years"),
                           (2, "50—59 years"),       (3, "60 years or older"),)


DIABETES_RISK_2_CHOICES = ((1, "Man"),(0, "Woman"), )
DIABETES_RISK_3_CHOICES = ((1, "Yes"),(0, "No"), )
DIABETES_RISK_4_CHOICES = ((1, "Yes"),(0, "No"), )
DIABETES_RISK_5_CHOICES = ((1, "Yes"),(0, "No"), )
DIABETES_RISK_6_CHOICES = ((0, "Yes"),(1, "No"), )
DIABETES_RISK_7_CHOICES = (#119-142 143-190 191+
                           (0, """4'10":  118 lbs or less"""),
                           (1, """4'10":  119-142 lbs"""),
                           (2, """4'10":  119-142 lbs"""),
                           (3, """4'10":  191 lbs or more"""),

                            #124-147 148-197 198+
                           (0, """4'11":  123 lbs or less"""),
                           (1, """4'11":  124-147 lbs"""),
                           (2, """4'11":  148-197 lbs"""),
                           (3, """4'11":  198 lbs or more"""),    
    
                           #128-152 153-203 204+
                           (0, """5'00":  127 lbs or less"""),
                           (1, """5'00":  128-152 lbs"""),
                           (2, """5'00":  153-203 lbs"""),
                           (3, """5'00":  204 lbs or more"""),
                           
                           #132-157 158-210 211+
                           (0, """5'01":  131 lbs or less"""),
                           (1, """5'01":  132-157 lbs"""),
                           (2, """5'01":  158-210 lbs"""),
                           (3, """5'01":  211 lbs or more"""),

                            #136-163 164-217 218+
                           (0, """5'02":  135 lbs or less"""),
                           (1, """5'02":  136-163 lbs"""),
                           (2, """5'02":  164-217 lbs"""),
                           (3, """5'02":  218 lbs or more"""),
                           
                           #141-168 169-224 225+
                           (0, """5'03":  140 lbs or less"""),
                           (1, """5'03":  141-168 lbs"""),
                           (2, """5'03":  169-224 lbs"""),
                           (3, """5'03":  225 lbs or more"""),
                           
                           #145-173 174-231 232+
                           (0, """5'04":  144 lbs or less"""),
                           (1, """5'04":  145-173 lbs"""),
                           (2, """5'04":  174-231 lbs"""),
                           (3, """5'04":  232 lbs or more"""),
                           
                           
                           #150-179 180-239 240+
                           (0, """5'05":  149 lbs or less"""),
                           (1, """5'05":  150-179 lbs"""),
                           (2, """5'05":  180-239 lbs"""),
                           (3, """5'05":  240 lbs or more"""),

                            #155-185 186-246 247+
                           (0, """5'06":  154 lbs or less"""),
                           (1, """5'06":  155-185 lbs"""),
                           (2, """5'06":  186-246 lbs"""),
                           (3, """5'06":  247 lbs or more"""),
                           
                           #159-190 191-254 255+
                           (0, """5'07":  158 lbs or less"""),
                           (1, """5'07":  159-190 lbs"""),
                           (2, """5'07":  191-254 lbs"""),
                           (3, """5'07":  255 lbs or more"""),
                           
                           #164-196 197-261 262+
                           (0, """5'08":  163 lbs or less"""),
                           (1, """5'08":  164-196 lbs"""),
                           (2, """5'08":  197-261 lbs"""),
                           (3, """5'08":  262 or more"""),
                           
                           #169-202 203-269 270+
                           (0, """5'09":  168 lbs or less"""),
                           (1, """5'09":  169-202 lbs"""),
                           (2, """5'09":  203-269 lbs"""),
                           (3, """5'09":  270 or more"""),

                            #174-208 209-277 278+
                           (0, """5'10":  173 lbs or less"""),
                           (1, """5'10":  174-208 lbs"""),
                           (2, """5'10":  209-277 lbs"""),
                           (3, """5'10":  278 or more"""),
                           
                           #179-214 215-285 286+
                           (0, """5'11":  178 lbs or less"""),
                           (1, """5'11":  179-214 lbs"""),
                           (2, """5'11":  215-285 lbs"""),
                           (3, """5'11":  286 or more"""),
                           
                           #184-220 221-293 294+
                           (0, """6'00":  183 lbs or less"""),
                           (1, """6'00":  184-220 lbs"""),
                           (2, """6'00":  221-293 lbs"""),
                           (3, """6'00":  294 or more"""),

                            #189-226 227-301 302+
                           (0, """6'01":  188 lbs or less"""),
                           (1, """6'01":  189-226 lbs"""),
                           (2, """6'01":  227-301 lbs"""),
                           (3, """6'01":  302 or more"""),
                           
                           #194-232 233-310 311+
                           (0, """6'02":  193 lbs or less"""),
                           (1, """6'02":  194-232 lbs"""),
                           (2, """6'02":  233-310 lbs"""),
                           (3, """6'02":  311 or more"""),
                           
                           #200-239 240-318 319+
                           (0, """6'04":  299 lbs or less"""),
                           (1, """6'04":  200-239 lbs"""),
                           (2, """6'04":  240-318 lbs"""),
                           (3, """6'04":  319 or more"""),
                           
                           #205-245 246-327 328+
                           (0, """6'04":  204 lbs or less"""),
                           (1, """6'04":  205-245 lbs"""),
                           (2, """6'04":  246-327 lbs"""),
                           (3, """6'04":  329 or more"""),
                        )




class ADAType2DiabetesScreen(models.Model):
    patient         = models.ForeignKey(PatientProfile)
    worker          = models.ForeignKey(User)
    creation_date   = models.DateField(default=datetime.date.today)
    risk_1  = models.IntegerField(max_length=1, choices=DIABETES_RISK_1_CHOICES,
                            verbose_name ="How old are you?")
    risk_2  = models.IntegerField(max_length=1, choices=DIABETES_RISK_2_CHOICES,
                            verbose_name ="Are you a man or a woman?")
    
    risk_3  = models.IntegerField(max_length=1, choices=DIABETES_RISK_3_CHOICES,
                            verbose_name ="If you are a woman, have you ever been diagnosed with gestational diabetes?")
    risk_4 = models.IntegerField(max_length=1, choices=DIABETES_RISK_4_CHOICES,
                            verbose_name ="Do you have a mother, father, sister, or brother with diabetes?")
    risk_5 = models.IntegerField(max_length=1, choices=DIABETES_RISK_6_CHOICES,
                            verbose_name ="Have you ever been diagnosed with high blood pressure?")
    risk_6 = models.IntegerField(max_length=1, choices=DIABETES_RISK_6_CHOICES,
                            verbose_name ="Are you physically active?")
    risk_7 = models.IntegerField(max_length=1, choices=DIABETES_RISK_7_CHOICES,
                            verbose_name ="What is your weight status?")
    
    risk_score          = models.IntegerField(max_length=2, editable=False, verbose_name="Score")
    recommend_followup  = models.BooleanField(default=False, verbose_name="Recommend Followup",
                                              editable=False)
    
    
    class Meta:
        unique_together = (("patient", "creation_date"),)
        get_latest_by   = "creation_date"
        ordering        = ('-creation_date',)
        
        
    def save(self, **kwargs):
        self.patient.ada_type2_diabetes_screen_complete = True
        self.patient.save()
        self.risk_score = self.risk_1 + self.risk_2 + self.risk_3 + \
                          self.risk_4 +  self.risk_5 + self.risk_6 + self.risk_7
     
        if self.risk_score >= 5:
            self.recommend_followup = True
        else:
            self.recommend_followup = False
        
        super(ADAType2DiabetesScreen, self).save(**kwargs)
