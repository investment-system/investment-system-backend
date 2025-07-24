from django.db.models.signals import post_save
from django.dispatch import receiver
from shares.models import ShareRecord
from profits.models import ProfitPayout
from transactions.models import Transaction
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal


@receiver(post_save, sender=ShareRecord)
def create_profit_payout(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        # Check if a payout already exists to avoid duplication
        if not ProfitPayout.objects.filter(share_record=instance).exists():
            original_transaction = instance.received_transaction

            # Create the profit payout
            payout = ProfitPayout.objects.create(
                transaction=original_transaction,
                share_record=instance,
                payout_type='pending',  # Admin can later update this
                profit_rate=instance.share_return_rate,
            )
