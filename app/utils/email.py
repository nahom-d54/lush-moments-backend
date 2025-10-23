import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

import aiosmtplib

from app.config import settings

logger = logging.getLogger(__name__)


async def send_email(
    to_email: str | List[str],
    subject: str,
    html_content: str,
    text_content: str = None,
) -> bool:
    """
    Send an email using SMTP.

    Args:
        to_email: Recipient email address or list of addresses
        subject: Email subject
        html_content: HTML content of the email
        text_content: Plain text content (fallback)

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # For development/testing without SMTP configured
        if not settings.SMTP_HOST or not settings.SMTP_USERNAME:
            logger.warning("SMTP not configured. Logging email instead of sending.")
            print(f"\n{'=' * 50}")
            print("EMAIL NOTIFICATION (SMTP NOT CONFIGURED)")
            print(f"{'=' * 50}")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"HTML Content:\n{html_content}")
            print(f"{'=' * 50}\n")
            return True

        # Create message
        message = MIMEMultipart("alternative")
        message["From"] = settings.SMTP_FROM_EMAIL
        message["To"] = to_email if isinstance(to_email, str) else ", ".join(to_email)
        message["Subject"] = subject

        # Add plain text version
        if text_content:
            part1 = MIMEText(text_content, "plain")
            message.attach(part1)

        # Add HTML version
        part2 = MIMEText(html_content, "html")
        message.attach(part2)

        # Send email
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD,
            use_tls=settings.SMTP_USE_TLS,
        )

        logger.info(f"Email sent successfully to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False


async def send_contact_form_notification(
    user_name: str, user_email: str, user_phone: str, message: str
) -> bool:
    """Send notification email when contact form is submitted"""

    business_phone = getattr(settings, "BUSINESS_PHONE", "N/A")
    admin_email = getattr(settings, "ADMIN_EMAIL", "admin@lushmoments.com")

    # Email to admin
    admin_subject = f"New Contact Form Submission from {user_name}"
    admin_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #4a5568; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">
                    New Contact Form Submission
                </h2>
                <div style="margin: 20px 0;">
                    <p><strong>Name:</strong> {user_name}</p>
                    <p><strong>Email:</strong> <a href="mailto:{user_email}">{user_email}</a></p>
                    <p><strong>Phone:</strong> {user_phone}</p>
                    <p><strong>Message:</strong></p>
                    <div style="background-color: #f7fafc; padding: 15px; border-left: 4px solid #4299e1; margin: 10px 0;">
                        {message}
                    </div>
                </div>
                <p style="color: #718096; font-size: 12px; margin-top: 20px;">
                    This is an automated notification from Lush Moments.
                </p>
            </div>
        </body>
    </html>
    """

    # Email to user (confirmation)
    user_subject = "Thank you for contacting Lush Moments!"
    user_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #4a5568; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">
                    Thank You for Reaching Out!
                </h2>
                <p>Hi {user_name},</p>
                <p>
                    Thank you for contacting <strong>Lush Moments</strong>. We have received your message and 
                    our team will get back to you within 24-48 hours.
                </p>
                <div style="background-color: #f7fafc; padding: 15px; border-left: 4px solid #48bb78; margin: 20px 0;">
                    <p><strong>Your Message:</strong></p>
                    <p>{message}</p>
                </div>
                <p>
                    If you have any urgent questions, feel free to call us at <strong>{business_phone}</strong>.
                </p>
                <p style="margin-top: 30px;">
                    Best regards,<br>
                    <strong>The Lush Moments Team</strong>
                </p>
                <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;">
                <p style="color: #718096; font-size: 12px;">
                    This is an automated confirmation email. Please do not reply to this email.
                </p>
            </div>
        </body>
    </html>
    """

    # Send both emails
    admin_sent = await send_email(admin_email, admin_subject, admin_html)
    user_sent = await send_email(user_email, user_subject, user_html)

    return admin_sent and user_sent


async def send_booking_confirmation(
    user_name: str,
    user_email: str,
    event_type: str,
    event_date: str,
    booking_id: int,
) -> bool:
    """Send confirmation email when booking is created"""

    business_phone = getattr(settings, "BUSINESS_PHONE", "N/A")
    admin_email = getattr(settings, "ADMIN_EMAIL", "admin@lushmoments.com")

    # Email to user
    user_subject = f"Booking Confirmation - {event_type}"
    user_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #4a5568; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">
                    Booking Confirmation
                </h2>
                <p>Hi {user_name},</p>
                <p>
                    Thank you for booking with <strong>Lush Moments</strong>! We're excited to help make your 
                    event unforgettable.
                </p>
                <div style="background-color: #f7fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #2d3748; margin-top: 0;">Booking Details</h3>
                    <p><strong>Booking ID:</strong> #{booking_id}</p>
                    <p><strong>Event Type:</strong> {event_type}</p>
                    <p><strong>Event Date:</strong> {event_date}</p>
                    <p><strong>Status:</strong> <span style="color: #d69e2e; font-weight: bold;">Pending Confirmation</span></p>
                </div>
                <p>
                    Our team will review your booking details and contact you within 24-48 hours to confirm 
                    availability and discuss next steps.
                </p>
                <p>
                    If you have any questions, feel free to contact us at <strong>{business_phone}</strong> 
                    or reply to this email.
                </p>
                <p style="margin-top: 30px;">
                    Best regards,<br>
                    <strong>The Lush Moments Team</strong>
                </p>
                <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;">
                <p style="color: #718096; font-size: 12px;">
                    Booking Reference: #{booking_id}
                </p>
            </div>
        </body>
    </html>
    """

    # Email to admin
    admin_subject = f"New Booking Request - {event_type} (#{booking_id})"
    admin_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #4a5568; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">
                    New Booking Request
                </h2>
                <div style="background-color: #f7fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Booking ID:</strong> #{booking_id}</p>
                    <p><strong>Client Name:</strong> {user_name}</p>
                    <p><strong>Email:</strong> <a href="mailto:{user_email}">{user_email}</a></p>
                    <p><strong>Event Type:</strong> {event_type}</p>
                    <p><strong>Event Date:</strong> {event_date}</p>
                </div>
                <p>
                    Please review this booking in the admin panel and contact the client to confirm.
                </p>
                <p style="color: #718096; font-size: 12px; margin-top: 20px;">
                    This is an automated notification from Lush Moments.
                </p>
            </div>
        </body>
    </html>
    """

    # Send both emails
    user_sent = await send_email(user_email, user_subject, user_html)
    admin_sent = await send_email(admin_email, admin_subject, admin_html)

    return user_sent and admin_sent


# Legacy function compatibility
async def send_admin_notification(
    event_type: str, date: str, venue: str, client_info: str
):
    """Send new booking notification to admin (legacy compatibility)"""
    admin_email = getattr(settings, "ADMIN_EMAIL", "admin@lushmoments.com")
    subject = "New Booking Received"
    body = f"""
    <html>
        <body>
            <h3>New booking received:</h3>
            <ul>
                <li>Event Type: {event_type}</li>
                <li>Date: {date}</li>
                <li>Venue: {venue}</li>
                <li>Client Info: {client_info}</li>
            </ul>
            <p>Please review and confirm the booking.</p>
        </body>
    </html>
    """
    await send_email(admin_email, subject, body)
