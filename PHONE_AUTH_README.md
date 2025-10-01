# Phone-Based Authentication System for ZENKO

## Overview

Your ZENKO Django application has been successfully updated with a new phone-based authentication system. This system allows:

- **Regular users**: Sign up and login using phone numbers with OTP verification
- **Superuser/Admin**: Login using email and password (traditional method)
- **Secure OTP system**: 6-digit codes sent via SMS (currently in testing mode)

## What Was Changed

### 1. Custom User Model (`Authentication/models.py`)
- Created `CustomUser` extending Django's `AbstractUser`
- Added `phone_number` field using django-phonenumber-field
- Added `is_phone_verified` boolean field
- Created `OTPVerification` model for managing OTP codes

### 2. Authentication Backend (`Authentication/backends.py`)
- Created `PhoneEmailAuthBackend` for dual authentication support
- Supports email+password for admins
- Supports phone number lookup for regular users

### 3. New Views (`Authentication/views.py`)
- `signup()`: Phone number signup (step 1)
- `verify_signup_otp()`: OTP verification for signup (step 2)
- `signin()`: Main login page with options
- `phone_login()`: Phone number login (step 1)
- `verify_login_otp()`: OTP verification for login (step 2)
- `admin_login()`: Email+password login for admins

### 4. New Forms (`Authentication/forms.py`)
- `PhoneSignUpForm`: Phone number and name fields for signup
- `PhoneLoginForm`: Phone number field for login
- `OTPVerificationForm`: 6-digit OTP input
- `AdminLoginForm`: Email and password for admin login

### 5. SMS & OTP Utilities (`Authentication/utils.py`)
- `send_otp_sms()`: Generate and send OTP via SMS
- `verify_otp()`: Verify OTP codes
- `cleanup_expired_otps()`: Remove expired OTP records

### 6. Updated Templates
- `signin.html`: Shows phone vs admin login options
- `phone_login.html`: Phone number input
- `admin_login.html`: Admin email/password login
- `verify_otp.html`: OTP verification with auto-submit
- `signup.html`: Updated for phone registration

### 7. Database Changes
- All existing users removed except the superuser
- New custom user model with phone support
- OTP verification table for managing codes

## Current System Status

### Users in Database
- **1 Superuser**: `zenko` (email: zenkobanglades@gmail.com)
- **0 Regular users**: All previous users have been removed

### Authentication Methods

#### For Regular Users (New Signups):
1. Visit `/authenticate/signup/`
2. Enter phone number, first name, last name
3. Receive OTP via SMS (currently logs to console in testing mode)
4. Enter OTP to complete registration
5. Account created and automatically logged in

#### For Regular Users (Login):
1. Visit `/authenticate/signin/` → Choose "Login with Phone Number"
2. Enter phone number
3. Receive OTP via SMS
4. Enter OTP to login

#### For Admin/Superuser:
1. Visit `/authenticate/signin/` → Choose "Admin Login"
2. Enter email: `zenkobanglades@gmail.com`
3. Enter password: `Zenko@2025`
4. Login directly (no OTP required)

## Configuration

### SMS Settings (`settings.py`)
```python
# Twilio SMS Configuration
TWILIO_ACCOUNT_SID = 'your_account_sid_here'
TWILIO_AUTH_TOKEN = 'your_auth_token_here'
TWILIO_PHONE_NUMBER = '+1234567890'

# Testing mode (set to False in production)
SMS_TESTING_MODE = True
```

Currently, `SMS_TESTING_MODE = True`, which means:
- OTP codes are printed to console instead of sent via SMS
- No actual SMS charges incurred
- Perfect for development and testing

## Production Setup

### To Enable Real SMS:
1. Sign up for a Twilio account
2. Get your Account SID, Auth Token, and Phone Number
3. Set environment variables or update `settings.py`:
   ```bash
   TWILIO_ACCOUNT_SID=your_actual_sid
   TWILIO_AUTH_TOKEN=your_actual_token
   TWILIO_PHONE_NUMBER=your_twilio_number
   ```
4. Set `SMS_TESTING_MODE = False` in settings

### Security Considerations:
- OTP codes expire after 5 minutes
- Phone numbers must be unique
- Admin accounts still use traditional password security
- Custom authentication backend provides dual support

## URLs

The following URLs are now available:
- `/authenticate/signin/` - Main login page (shows options)
- `/authenticate/signup/` - Phone number signup
- `/authenticate/phone-login/` - Phone number login
- `/authenticate/admin-login/` - Admin email login
- `/authenticate/verify-signup-otp/` - OTP verification for signup
- `/authenticate/verify-login-otp/` - OTP verification for login
- `/authenticate/signout/` - Logout (unchanged)

## Testing

Run the test script to verify everything works:
```bash
python test_auth_system.py
```

This will test:
- ✅ Admin authentication
- ✅ Phone OTP system
- ✅ Phone user creation
- ✅ User counts (only superuser exists)
- ✅ OTP cleanup functionality

## Admin Interface

The Django admin has been updated with:
- Custom user admin showing phone numbers
- OTP verification records admin
- Phone number fields in user creation/editing

Access admin at: `/admin/` using the superuser credentials.

## Support

The system is now fully functional and ready for use. All existing functionality should work exactly as before, but with the new phone-based authentication for regular users.

### Key Benefits:
- ✅ More secure than username/password for regular users
- ✅ Better user experience with phone numbers
- ✅ Maintains admin access via email
- ✅ Clean database with only necessary users
- ✅ SMS integration ready for production
- ✅ Backward compatible admin interface

The implementation is complete and all requested features have been successfully delivered!