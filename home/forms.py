# home/forms.py
from django import forms # type: ignore
from django.contrib.auth.models import User # type: ignore
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address']

class CheckoutForm(forms.Form):
    country_choices = [
        ('', 'Select an option'),
        ('inside_dhaka', 'Inside Dhaka'),
        ('outside_dhaka', 'Outside Dhaka'),
    ]

    country = forms.ChoiceField(choices=country_choices, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    order_notes = forms.CharField(widget=forms.Textarea, required=False)