from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone
from django.db import IntegrityError, transaction


class AdminManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Admins must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Administrator(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('viewer', 'Viewer'),
    ]

    POSITION_CHOICES = [
        ('manager', 'Manager'),
        ('staff', 'Staff'),
        ('executive', 'Executive'),
    ]

    admin_code = models.CharField(max_length=30, unique=True, blank=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    ic_number = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='admin_profiles/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AdminManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # full_name is now optional

    groups = models.ManyToManyField(
        Group,
        related_name='administrator_users',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='administrator_user_permissions',
        blank=True
    )

    def __str__(self):
        return self.email

    def generate_admin_code(self):
        today = timezone.now().strftime("%Y%m%d")
        prefix = "AKM"
        count_today = Administrator.objects.filter(
            created_at__date=timezone.now().date()
        ).count() + 1
        return f"{prefix}-{today}-{count_today:04d}"

    def save(self, *args, **kwargs):
        if not self.admin_code:
            for attempt in range(5):  # retry max 5 times
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
