from django.contrib import admin
from models import PatientProfile, Visit
from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail import default
ADMIN_THUMBS_SIZE = '60x60'




class PatientProfileAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('patient_id', 'worker', 'gender', 'first_name', 'last_name', 'creation_date')
    search_fields = ('patient_id', 'gender', 'last_name', 'first_name', 'creation_date')


admin.site.register(PatientProfile, PatientProfileAdmin)
admin.site.register(Visit)
