from django.contrib import admin
from models import Linkage, Referral, LinkageFollowUp

class LinkageFollowUpAdmin(admin.ModelAdmin):
    list_display = ('worker', 'service', 'activity_type', 'creation_date')
    search_fields = ['patient__patient_id', 'worker', 'creation_date']
admin.site.register(LinkageFollowUp, LinkageFollowUpAdmin)


class LinkageAdmin(admin.ModelAdmin):
    list_display = ('patient','worker', 'referral_type', 'creation_date')
    search_fields = ['patient__patient_id', 'referral_type', 'creation_date']
admin.site.register(Linkage, LinkageAdmin)

class ReferralAdmin(admin.ModelAdmin):
    list_display = ('patient','worker', 'referral_type', 'creation_date')
    search_fields = ['patient__patient_id', 'referral_type', 'creation_date']

admin.site.register(Referral, ReferralAdmin)