from django.db.models.signals import post_save
from django.dispatch import receiver
from transactions.models import Transaction
from .models import RegistrationPayment
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Transaction)
def create_registration_payment(sender, instance, created, **kwargs):
    if created and instance.source_type == 'registration_payments':
        payment, created_payment = RegistrationPayment.objects.get_or_create(
            transaction=instance,
            defaults={'member': instance.member}
        )

        # ✅ Send email only if it was just created
        if created_payment and payment.member and payment.member.email:
            subject = "Registration Payment Confirmation"

            message = (

                f"Dear {payment.member.full_name},\n\n"
                f"We are pleased to inform you that we have successfully received your registration payment for the Koperasi Masjid investment platform.\n\n"
                f"Below are the details of your payment:\n"
                f"----------------------------------------\n"
                f"• Payment Amount : RM {payment.transaction.amount:.2f}\n"
                f"• Payment Date   : {payment.confirmed_at.strftime('%d %B %Y')}\n"
                f"----------------------------------------\n\n"
                f"If you have any questions or need further assistance, please do not hesitate to reach out to our support team.\n\n"
                f"Thank you for your trust and commitment. We look forward to serving you as part of the Koperasi Masjid community.\n\n"
                f"Warm regards,\n"
                f"Koperasi Masjid Team"

            )

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [payment.member.email],
                fail_silently=False,
            )
