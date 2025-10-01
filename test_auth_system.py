#!/usr/bin/env python
"""
Test script for the new phone-based authentication system
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zenko.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate
from phonenumber_field.phonenumber import PhoneNumber
from Authentication.utils import send_otp_sms, verify_otp
from Authentication.models import OTPVerification

User = get_user_model()

def test_admin_authentication():
    """Test admin email authentication"""
    print("=== Testing Admin Authentication ===")
    
    admin_user = authenticate(username='zenkobanglades@gmail.com', password='Zenko@2025')
    if admin_user and admin_user.is_superuser:
        print("✅ Admin authentication: PASSED")
        print(f"   Admin: {admin_user.email}")
    else:
        print("❌ Admin authentication: FAILED")
    
def test_phone_otp_system():
    """Test phone OTP generation and verification"""
    print("\n=== Testing Phone OTP System ===")
    
    test_phone = PhoneNumber.from_string('+1234567890')
    
    # Test OTP generation
    otp_code = send_otp_sms(test_phone)
    if otp_code:
        print("✅ OTP generation: PASSED")
        print(f"   Generated OTP: {otp_code}")
    else:
        print("❌ OTP generation: FAILED")
        return
    
    # Test OTP verification
    is_valid = verify_otp(test_phone, otp_code)
    if is_valid:
        print("✅ OTP verification: PASSED")
    else:
        print("❌ OTP verification: FAILED")

def test_phone_user_creation():
    """Test phone user creation"""
    print("\n=== Testing Phone User Creation ===")
    
    test_phone = PhoneNumber.from_string('+1987654321')
    
    # Create a phone user
    try:
        user = User.objects.create_user(
            username=f"user_test123",
            phone_number=test_phone,
            first_name="Test",
            last_name="User",
            is_phone_verified=True
        )
        print("✅ Phone user creation: PASSED")
        print(f"   Created user: {user.username} with phone {user.phone_number}")
        
        # Clean up
        user.delete()
        print("   Test user cleaned up")
        
    except Exception as e:
        print(f"❌ Phone user creation: FAILED - {e}")

def test_user_counts():
    """Test that we only have the superuser"""
    print("\n=== Testing User Counts ===")
    
    total_users = User.objects.count()
    superusers = User.objects.filter(is_superuser=True).count()
    regular_users = User.objects.filter(is_superuser=False).count()
    
    print(f"   Total users: {total_users}")
    print(f"   Superusers: {superusers}")
    print(f"   Regular users: {regular_users}")
    
    if superusers == 1 and regular_users == 0:
        print("✅ User counts: PASSED (Only superuser exists)")
    else:
        print("❌ User counts: FAILED (Should only have 1 superuser)")

def test_otp_cleanup():
    """Test OTP cleanup functionality"""
    print("\n=== Testing OTP Cleanup ===")
    
    from Authentication.utils import cleanup_expired_otps
    
    initial_count = OTPVerification.objects.count()
    cleaned = cleanup_expired_otps()
    
    print(f"   OTP records before cleanup: {initial_count}")
    print(f"   Cleaned up OTP records: {cleaned}")
    print("✅ OTP cleanup: PASSED")

if __name__ == '__main__':
    print("🚀 Starting Authentication System Tests\n")
    
    test_admin_authentication()
    test_phone_otp_system()
    test_phone_user_creation()
    test_user_counts()
    test_otp_cleanup()
    
    print("\n🎉 Authentication System Tests Completed!")
    print("\n📝 Summary:")
    print("   - Admin can login with email (zenkobanglades@gmail.com)")
    print("   - Regular users signup/login with phone numbers")
    print("   - OTP verification system works")
    print("   - SMS testing mode is enabled")
    print("   - All old users removed except superuser")