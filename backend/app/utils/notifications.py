import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.config import get_settings

settings = get_settings()


async def send_email_notification(
    to_email: str,
    subject: str,
    body: str,
    html_body: Optional[str] = None
) -> bool:
    """Send email notification."""
    # Placeholder - implement with your email service
    print(f"Email to {to_email}: {subject}")
    return True


async def send_visitor_notification(
    resident_email: str,
    visitor_name: str,
    action: str
) -> bool:
    """Send visitor entry/exit notification to resident."""
    subject = f"Visitor {action.title()}: {visitor_name}"
    body = f"Your visitor {visitor_name} has {action} the premises."
    return await send_email_notification(resident_email, subject, body)


async def send_delivery_notification(
    resident_email: str,
    courier_company: str,
    tracking_number: str
) -> bool:
    """Send delivery arrival notification."""
    subject = f"Delivery Arrived: {courier_company}"
    body = f"A package from {courier_company} (Tracking: {tracking_number}) has arrived at the gate."
    return await send_email_notification(resident_email, subject, body)


async def send_emergency_notification(
    emails: list,
    alert_type: str,
    title: str,
    description: str
) -> bool:
    """Send emergency alert to multiple recipients."""
    subject = f"🚨 Emergency Alert: {alert_type.upper()} - {title}"
    body = f"Emergency Alert\nType: {alert_type}\nTitle: {title}\nDescription: {description}"
    
    for email in emails:
        await send_email_notification(email, subject, body)
    return True
