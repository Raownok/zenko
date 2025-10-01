from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class PhoneEmailAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows login with:
    - Email + password for superusers
    - Phone number + OTP for regular users
    - Username + password (fallback)
    """
    
    def authenticate(self, request, username=None, password=None, phone_number=None, **kwargs):
        if username is None and phone_number is None:
            return None
            
        try:
            if phone_number:
                # Phone number authentication (for regular users)
                user = User.objects.get(phone_number=phone_number)
                # Note: For phone auth, OTP verification should be handled in the view
                # This backend just finds the user by phone number
                return user
            else:
                # Email or username authentication (mainly for superusers)
                user = User.objects.get(
                    Q(email=username) | Q(username=username)
                )
                
                # Check password
                if user.check_password(password):
                    return user
                    
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # Handle multiple users with same email (shouldn't happen with unique constraint)
            return None
            
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None