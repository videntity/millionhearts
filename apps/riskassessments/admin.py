from django.contrib import admin
from models import Framingham10yrHeartRiskTest, CardioDiabetesRiskTest, \
                   CAGEAIDSubstanceAbuseScreen, ADAType2DiabetesScreen, \
                   ArchimedesRiskAssessment


class ArchimedesRiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'creation_date')
    search_fields = ['patient_id', 'creation_date']
admin.site.register(ArchimedesRiskAssessment,
                    ArchimedesRiskAssessmentAdmin)



class ADAType2DiabetesScreenAdmin(admin.ModelAdmin):
    list_display = ('patient','worker', 'risk_score', 'recommend_followup',
                    'creation_date')
    search_fields = ['patient__patient_id', 'creation_date']
admin.site.register(ADAType2DiabetesScreen,
                    ADAType2DiabetesScreenAdmin)


class CAGEAIDSubstanceAbuseScreenAdmin(admin.ModelAdmin):
    list_display = ('patient','worker', 'cage_score', 'recommend_followup',
                    'creation_date')
    search_fields = ['patient__patient_id', 'creation_date']
admin.site.register(CAGEAIDSubstanceAbuseScreen,
                    CAGEAIDSubstanceAbuseScreenAdmin)


class Framingham10yrHeartRiskTestAdmin(admin.ModelAdmin):
    list_display = ('patient','worker', 'percent_risk', 'creation_date')
    search_fields = ['patient__patient_id', 'creation_date']
admin.site.register(Framingham10yrHeartRiskTest,
                    Framingham10yrHeartRiskTestAdmin)



class CardioDiabetesRiskTestAdmin(admin.ModelAdmin):
    list_display = ('patient','worker', 'risk_list', 'creation_date')
    search_fields = ['patient__patient_id', 'creation_date']
admin.site.register(CardioDiabetesRiskTest, CardioDiabetesRiskTestAdmin)