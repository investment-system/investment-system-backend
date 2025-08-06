import random
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models, IntegrityError, transaction
from datetime import date, timedelta
from django.utils import timezone

def default_share_date():
    return date.today()


class MemberManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self.create_user(email, password, **extra_fields)

class Member(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )

    REGISTRATION_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]

    MEMBER_CODE_PREFIX = "MKM"

    member_code = models.CharField(max_length=30, unique=True, blank=True)
    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=255, blank=True, null=True, default="")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    ic_number = models.CharField(max_length=255, blank=True, null=True, default="")
    date_of_birth = models.DateField(blank=True, null=True, default=None)
    phone_number = models.CharField(max_length=20, blank=True, null=True, default="")
    country = models.CharField(max_length=100, blank=True, null=True, default="Malaysia")
    address_line = models.CharField(max_length=255, blank=True, null=True, default="")
    city = models.CharField(max_length=100, blank=True, null=True, default="")
    state = models.CharField(max_length=100, blank=True, null=True, default="")

    bank_name = models.CharField(max_length=100, blank=True, null=True, default="")
    account_holder_name = models.CharField(max_length=255, blank=True, null=True, default="")
    bank_account_number = models.CharField(max_length=100, blank=True, null=True, default="")

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    registration_status = models.CharField( max_length=10, choices=REGISTRATION_STATUS_CHOICES, default='unpaid')

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_created_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)


    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.full_name or ''} <{self.email}>"

    def generate_member_code(self):
        today = timezone.now().strftime("%Y%m%d")
        count_today = Member.objects.filter(date_joined__date=timezone.now().date()).count() + 1
        return f"{self.MEMBER_CODE_PREFIX}-{today}-{count_today:04d}"

    def generate_verification_code(self):
        self.verification_code = f"{random.randint(100000, 999999)}"
        self.code_created_at = timezone.now()
        self.save()

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
