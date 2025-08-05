from django.db.models.signals import post_save
from django.dispatch import receiver
from transactions.models import Transaction
from shares.models import ShareRecord
from datetime import timedelta, date

@receiver(post_save, sender=Transaction)
def create_share_record_if_needed(sender, instance, created, **kwargs):
    if created and instance.source_type == 'share':
        ShareRecord.objects.create(
            member=instance.member,
            project_name='KKM',
            share_return_rate=10.0,
            received_transaction=instance,
            share_date=date.today(),
            expected_share_maturity_date=date.today() + timedelta(days=365),
            share_duration_days=365,
            status='active'
        )
