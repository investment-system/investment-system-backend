from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import User
from .models import Member

@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == 'member':
        Member.objects.create(user=instance)
        print(f"Created member profile for {instance.email}")  # Debugging