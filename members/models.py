from django.db import models
from authentication.models import User
from django.utils import timezone
from django.db import IntegrityError, transaction

class Member(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )

    REGISTRATION_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]

    MEMBER_CODE_PREFIX = "MKM"

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    member_code = models.CharField(max_length=30, unique=True, blank=True)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    ic_number = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True, default="Malaysia")
    address_line = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_holder_name = models.CharField(max_length=255, blank=True, null=True)
    bank_account_number = models.CharField(max_length=100, blank=True, null=True)

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    registration_status = models.CharField(max_length=10, choices=REGISTRATION_STATUS_CHOICES, default='unpaid')

    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_created_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} ({self.member_code})"

    def generate_member_code(self):
        today = timezone.now().strftime("%Y%m%d")
        count_today = Member.objects.filter(created_at__date=timezone.now().date()).count() + 1
        return f"{self.MEMBER_CODE_PREFIX}-{today}-{count_today:04d}"

    def save(self, *args, **kwargs):
        if not self.member_code:
            for attempt in range(5):
                try:
                    self.member_code = self.generate_member_code()
                    with transaction.atomic():
                        super().save(*args, **kwargs)
                    return
                except IntegrityError:
                    continue
            raise IntegrityError("Failed to generate a unique member_code after multiple attempts.")
        else:
            super().save(*args, **kwargs)

    @property
    def email(self):
        """Easy access to the user's email"""
        return self.user.email if hasattr(self, 'user') else None

    @property
    def full_name(self):
        """Easy access to the user's full name"""
        return self.user.full_name if hasattr(self, 'user') else None
