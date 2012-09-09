from django.contrib import admin
from models import SMSAppointmentReminder, SMSAdherenceReminder, SMSAdherenceTransaction

admin.site.register(SMSAppointmentReminder)
admin.site.register(SMSAdherenceReminder)
admin.site.register(SMSAdherenceTransaction)