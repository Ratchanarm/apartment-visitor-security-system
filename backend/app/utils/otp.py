import random
import string
from datetime import datetime, timedelta
from typing import Optional
from twilio.rest import Client
from app.config import get_settings

settings = get_settings()


def generate_otp(length: int = 6) -> str:
    """Generate a random numeric OTP."""
    return ''.join(random.choices(string.digits, k=length))


def get_otp_expiry(minutes: int = 10) -> datetime:
    """Get OTP expiry timestamp."""
    return datetime.utcnow() + timedelta(minutes=minutes)


def verify_otp(stored_otp: str, provided_otp: str, expiry: datetime) -> bool:
    """Verify OTP is correct and not expired."""
    if datetime.utcnow() > expiry:
        return False
    return stored_otp == provided_otp


def send_otp_sms(phone: str, otp: str) -> bool:
    """Send OTP via SMS using Twilio."""
    if not all([settings.twilio_account_sid, settings.twilio_auth_token]):
        print(f"SMS not configured. OTP for {phone}: {otp}")
        return True
    
    try:
        client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        message = client.messages.create(
            body=f"Your visitor verification OTP is: {otp}. Valid for 10 minutes.",
            from_=settings.twilio_phone_number,
            to=phone
        )
        return True
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return False
