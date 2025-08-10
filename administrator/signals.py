from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import User
from .models import Administrator

@receiver(post_save, sender=User)
def create_admin_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == 'admin':
        Administrator.objects.create(user=instance)