from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings


def send_verification_email(user):
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=user.email,
        subject="Verify Your Account",
        html_content=f"""
            Hi {user.full_name or user.email},<br><br>
            Your verification code is: <strong>{user.verification_code}</strong><br>
            This code expires in 10 minutes.
        """
    )
    sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    sg.send(message)
