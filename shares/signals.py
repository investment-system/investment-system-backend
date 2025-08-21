
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from shares.models import ShareRecord
from profits.models import ProfitPayout
from cancels.models import CancellationRecord

@receiver(post_save, sender=ShareRecord)
def handle_profit_payout(sender, instance, created, **kwargs):
    today = date.today()

    if instance.profit_payout_created:
        return

    # If status is completed, create profit payout
    if instance.status == 'completed':
        create_profit_payout(instance)

    # Auto-complete if maturity reached
    elif instance.status == 'active' and instance.expected_share_maturity_date == today:
        instance.status = 'completed'
        instance.save(update_fields=['status'])

def create_profit_payout(share):
    if not ProfitPayout.objects.filter(share_record=share).exists():
        ProfitPayout.objects.create(
            share_record=share,
            transaction=share.received_transaction,
            payout_type='pending',
            profit_rate=share.share_return_rate,
        )
        share.profit_payout_created = True
        share.save(update_fields=['profit_payout_created'])

@receiver(post_save, sender=ShareRecord)
def handle_cancellation_record(sender, instance, **kwargs):
    if instance.status == 'canceled':
        CancellationRecord.objects.get_or_create(share=instance)
