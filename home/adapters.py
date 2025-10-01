# home/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import Profile

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """
        Override save_user to create/update Profile automatically
        when logging in via Google.
        """
        user = super().save_user(request, sociallogin, form)

        # Get user's full name from Google
        data = sociallogin.account.extra_data
        full_name = data.get('name', '')

        # Ensure profile exists
        profile, created = Profile.objects.get_or_create(user=user)
        profile.full_name = full_name
        profile.save()

        return user
