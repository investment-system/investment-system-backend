from django.db import models
from authentication.models import User
from django.utils import timezone
from django.db import IntegrityError, transaction

class Administrator(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
    ]

    POSITION_CHOICES = [
        ('manager', 'Manager'),
        ('staff', 'Staff'),
        ('executive', 'Executive'),
    ]

    ADMIN_CODE_PREFIX = "AKM"

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    admin_code = models.CharField(max_length=30, unique=True, blank=True)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    ic_number = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='admin_profiles/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} ({self.admin_code})"

    def generate_admin_code(self):
        today = timezone.now().strftime("%Y%m%d")
        count_today = Administrator.objects.filter(created_at__date=timezone.now().date()).count() + 1
        return f"{self.ADMIN_CODE_PREFIX}-{today}-{count_today:04d}"

    def save(self, *args, **kwargs):
        if not self.admin_code:
            for attempt in range(5):
                try:
                    self.admin_code = self.generate_admin_code()
                    with transaction.atomic():
                        super().save(*args, **kwargs)
                    return
                except IntegrityError:
                    continue
            raise IntegrityError("Failed to generate a unique admin_code after multiple attempts.")
        else:
            super().save(*args, **kwargs)