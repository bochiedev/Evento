from django.contrib import admin
from accounts.models import OTP

# Register your models here.

class OTPAdmin(admin.ModelAdmin):
    list_display = ['code', 'username', 'secret', 'created_on']


admin.site.register(OTP, OTPAdmin)
