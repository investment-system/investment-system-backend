from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.user_type == "member":
        subject = "Welcome to Our Platform!"
        message = (
            "Welcome to Our Platform!\n\n"
            "Your account has been created successfully! We’re excited to have you on board.\n"
            "Please check your registered email for setup guidelines and activation instructions.\n\n"
            "Complete Your Membership Activation.\n"
            "Simply scan the QR code below to make a secure bank transfer.\n"
            "Don’t forget to keep your payment receipt for confirmation.\n"
            "Your account is protected with industry-standard encryption.\n\n"
            "Need help? Contact our support team at support@koperasimasjid2u.com.\n"
            f"Warm regards,\n"
            f"Koperasi Masjid Team"

        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )
