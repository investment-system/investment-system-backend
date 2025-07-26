from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models, IntegrityError, transaction
from django.utils import timezone


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
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class Member(AbstractBaseUser, PermissionsMixin):
    MEMBER_CODE_PREFIX = "MBR"

    member_code = models.CharField(max_length=30, unique=True, blank=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.full_name or ''} <{self.email}>"

    def generate_member_code(self):
        today = timezone.now().strftime("%Y%m%d")
        count_today = Member.objects.filter(
            date_joined__date=timezone.now().date()
        ).count() + 1
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
