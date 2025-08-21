from django.db.models.signals import post_save
from django.dispatch import receiver
from shares.models import ShareRecord
from .models import CancellationRecord

@receiver(post_save, sender=ShareRecord)
def handle_cancellation_record(sender, instance, created, **kwargs):
    if instance.status == 'canceled':
        # Check if a CancellationRecord already exists
        CancellationRecord.objects.get_or_create(share=instance)
