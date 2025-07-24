from django.db.models.signals import post_save
from django.dispatch import receiver
from shares.models import ShareRecord
from profits.models import ProfitPayout

@receiver(post_save, sender=ShareRecord)
def create_profit_payout(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        if not ProfitPayout.objects.filter(share_record=instance).exists():
            original_transaction = instance.received_transaction

            ProfitPayout.objects.create(
                transaction=original_transaction,
                share_record=instance,
                payout_type='pending',
                profit_rate=instance.share_return_rate,
            )
