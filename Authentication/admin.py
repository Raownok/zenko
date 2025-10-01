from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTPVerification

class CustomUserAdmin(UserAdmin):
    """Admin interface for CustomUser"""
    list_display = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_phone_verified')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_phone_verified')
    search_fields = ('username', 'email', 'phone_number', 'first_name', 'last_name')
    ordering = ('username',)
    
    # Add phone_number to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Phone Authentication', {'fields': ('phone_number', 'is_phone_verified')}),
    )
    
    # Add phone_number to add_fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Phone Authentication', {'fields': ('phone_number', 'is_phone_verified')}),
    )

class OTPVerificationAdmin(admin.ModelAdmin):
    """Admin interface for OTP verification"""
    list_display = ('phone_number', 'otp_code', 'created_at', 'is_verified')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('phone_number',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

# Register the models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTPVerification, OTPVerificationAdmin)
