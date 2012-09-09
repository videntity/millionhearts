from django.db import models
from django.contrib.localflavor.us.us_states import US_STATES
from django.contrib.localflavor.us.models import PhoneNumberField
from django.contrib.auth.models import User

WARD_CHOICES=(('1','1'), ('2','2'), ('3','3'),
    ('4','4'), ('5','5'),('6','6'),('7','7'),('8','8'),)

class LocationSetup(models.Model):
    
    address1    = models.CharField(max_length=100, verbose_name='Address', unique=True)
    address2    = models.CharField(max_length=100,blank=True,
                                                   verbose_name='Address Line 2')
    city        = models.CharField(max_length=100, default="Washington", verbose_name='City')
    state       = models.CharField(max_length=2, choices=US_STATES,
                        default="DC",verbose_name='State')
    zip         = models.CharField(max_length=10, verbose_name='Zip Code')
    
    ward        = models.CharField(max_length=2, verbose_name='Ward',
                        choices=WARD_CHOICES,) 
    
    
    def __unicode__(self):
        return '%s %s %s, %s (Ward:%s)' % (self.address1,
                                        self.address2,
                                        self.state,
                                        self.zip, self.ward)
