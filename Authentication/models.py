from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import random
from datetime import datetime, timedelta
from django.utils import timezone

class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    
    # For superusers, they will use email. For regular users, phone_number
    def save(self, *args, **kwargs):
        # If this is a superuser, we don't require phone verification
        if self.is_superuser:
            self.is_phone_verified = True
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.is_superuser:
            return f"Admin: {self.email}"
        return f"User: {self.phone_number or self.username}"

class OTPVerification(models.Model):
    phone_number = PhoneNumberField()
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def is_valid(self):
        """Check if OTP is still valid (5 minutes)"""
        return timezone.now() < self.created_at + timedelta(minutes=5)
    
    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP"""
        return str(random.randint(100000, 999999))
    
    def __str__(self):
        return f"OTP for {self.phone_number}: {self.otp_code}"