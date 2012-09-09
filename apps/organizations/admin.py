from django.contrib import admin
from models import Organization, Service,  Provider, PatientCareTeam

class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    #list_display = ('slug', )
class OrganizationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    #list_display = ('slug', )
    

admin.site.register(Service, ServiceAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Provider)
admin.site.register(PatientCareTeam)