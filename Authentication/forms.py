from django import forms
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField
from .models import OTPVerification

User = get_user_model()

class PhoneSignUpForm(forms.Form):
    """Form for phone number signup"""
    phone_number = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1234567890',
            'required': True
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('A user with this phone number already exists.')
        return phone_number

class OTPVerificationForm(forms.Form):
    """Form for OTP verification"""
    otp_code = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': '000000',
            'maxlength': '6',
            'pattern': '[0-9]{6}',
            'title': 'Please enter a 6-digit OTP code'
        })
    )

class PhoneLoginForm(forms.Form):
    """Form for phone number login"""
    phone_number = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1234567890',
            'required': True
        })
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('No account found with this phone number.')
        return phone_number

class AdminLoginForm(forms.Form):
    """Form for admin email login"""
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'admin@example.com'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
