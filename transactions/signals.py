from django.db.models.signals import post_save
from django.dispatch import receiver
from transactions.models import Transaction
from shares.models import ShareRecord
from datetime import timedelta, date
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal

@receiver(post_save, sender=Transaction)
def handle_share_transaction(sender, instance, created, **kwargs):

    if not created or instance.source_type != 'share':
        return

    member = instance.member

    # ✅ Check if this member already has a registration payment
    already_registered = Transaction.objects.filter(
        member=member, source_type="registration_payments"
    ).exists()

    if not already_registered:
        # If share amount is at least 50, split it
        if instance.amount >= Decimal("50.00"):
            # Create registration payment
            Transaction.objects.create(
                member=member,
                source_type="registration_payments",
                direction="in",
                amount=Decimal("50.00"),
                payment_method=instance.payment_method,
            )

            # Deduct 50 from current share amount
            instance.amount = instance.amount - Decimal("50.00")
            instance.save(update_fields=["amount"])
        else:
            # Not enough to cover registration
            return

    # ✅ Now create the ShareRecord for the remaining share amount
    share_record = ShareRecord.objects.create(
        member=instance.member,
        project_name='Katering Koperasi Masjid',
        share_return_rate=10.0,
        received_transaction=instance,
        share_date=date.today(),
        expected_share_maturity_date=date.today() + timedelta(days=365),
        share_duration_days=365,
        status='pending'
    )

    if member and hasattr(member, 'user') and member.user.email:
        subject = 'Your Share Purchase Has Been Confirmed'
        message = (
            f"Dear {member.user.full_name},\n\n"
            f"We are pleased to confirm the successful purchase of your share under the '{share_record.project_name}' project.\n\n"
            f"Below are the details of your share investment:\n"
            f"- Investment Amount: RM {instance.amount:.2f}\n"
            f"- Expected Return Rate: {share_record.share_return_rate}%\n"
            f"- Share Start Date: {share_record.share_date.strftime('%d %B %Y')}\n"
            f"- Maturity Date: {share_record.expected_share_maturity_date.strftime('%d %B %Y')}\n\n"
            f"If you have any questions or require further assistance, please do not hesitate to contact our team.\n\n"
            f"Thank you for your trust and continued support.\n\n"
            f"Best regards,\n"
            f"Koperasi Team"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [member.user.email],
            fail_silently=False,
        )
