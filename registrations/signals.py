from django.db.models.signals import post_save
from django.dispatch import receiver
from transactions.models import Transaction
from .models import RegistrationPayment

@receiver(post_save, sender=Transaction)
def create_registration_payment(sender, instance, created, **kwargs):
    if created and instance.source_type == 'registration_payments':
        RegistrationPayment.objects.get_or_create(
            transaction=instance,
            defaults={'member_id': instance.member_id}
        )
