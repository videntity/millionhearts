from django.contrib import admin
from models import UserProfile, ValidPasswordResetKey


admin.site.register(UserProfile)
admin.site.register(ValidPasswordResetKey)