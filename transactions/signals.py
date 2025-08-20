from django.db.models.signals import post_save
from django.dispatch import receiver
from transactions.models import Transaction
from shares.models import ShareRecord
from datetime import timedelta, date
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Transaction)
def create_share_record_if_needed(sender, instance, created, **kwargs):
    if created and instance.source_type == 'share':
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

        # ✅ Send email notification to the member
        member = instance.member
        if member and hasattr(member, 'user') and member.user.email:  # Updated this line
            subject = 'Your Share Purchase Has Been Confirmed'
            message = (
                f"Dear {member.user.full_name},\n\n"  # Updated to use member.user
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
                [member.user.email],  # Updated to use member.user.email
                fail_silently=False,
            )