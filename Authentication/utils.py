from twilio.rest import Client
from django.conf import settings
from .models import OTPVerification
import logging

logger = logging.getLogger(__name__)

def send_otp_sms(phone_number):
    """
    Generate and send OTP via SMS to the provided phone number.
    Returns the OTP code if successful, None if failed.
    """
    try:
        # Generate OTP
        otp_code = OTPVerification.generate_otp()
        
        # Save OTP to database
        otp_record = OTPVerification.objects.create(
            phone_number=phone_number,
            otp_code=otp_code
        )
        
        # Send SMS (if not in testing mode)
        if not settings.SMS_TESTING_MODE:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            message = client.messages.create(
                body=f"Your Zenko verification code is: {otp_code}. Valid for 5 minutes.",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=str(phone_number)
            )
            
            logger.info(f"SMS sent successfully to {phone_number}. Message SID: {message.sid}")
        else:
            # In testing mode, just log the OTP
            logger.info(f"Testing mode: OTP for {phone_number} is {otp_code}")
            print(f"Testing mode: OTP for {phone_number} is {otp_code}")
        
        return otp_code
        
    except Exception as e:
        logger.error(f"Failed to send OTP to {phone_number}: {str(e)}")
        return None

def verify_otp(phone_number, otp_code):
    """
    Verify the OTP code for the given phone number.
    Returns True if valid, False if invalid or expired.
    """
    try:
        # Get the most recent OTP for this phone number
        otp_record = OTPVerification.objects.filter(
            phone_number=phone_number,
            otp_code=otp_code,
            is_verified=False
        ).first()
        
        if not otp_record:
            return False
        
        # Check if OTP is still valid (not expired)
        if not otp_record.is_valid():
            return False
        
        # Mark as verified
        otp_record.is_verified = True
        otp_record.save()
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to verify OTP for {phone_number}: {str(e)}")
        return False

def cleanup_expired_otps():
    """
    Remove expired OTP records from database.
    This can be called periodically via a management command or cron job.
    """
    from django.utils import timezone
    from datetime import timedelta
    
    expired_threshold = timezone.now() - timedelta(minutes=5)
    expired_otps = OTPVerification.objects.filter(created_at__lt=expired_threshold)
    count = expired_otps.count()
    expired_otps.delete()
    
    logger.info(f"Cleaned up {count} expired OTP records")
    return count