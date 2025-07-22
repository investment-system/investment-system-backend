from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    POSITION_CHOICES = (
        ('director', 'Director'),
        ('officer', 'Officer'),
        ('auditor', 'Auditor'),
    )

    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.TextField(blank=True, null=True)

    full_name = models.CharField(max_length=255)
    ic_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)

    country = models.CharField(max_length=100, blank=True, null=True)
    address_line = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_holder_name = models.CharField(max_length=255, blank=True, null=True)
    bank_account_number = models.CharField(max_length=100, blank=True, null=True)

    profile_picture = models.TextField(blank=True, null=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    position = models.CharField(max_length=100, choices=POSITION_CHOICES, blank=True, null=True)  # for admins only

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # for Django admin
    last_login = models.DateTimeField(null=True, blank=True)
    activated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']

    objects = UserManager()

    def __str__(self):
        return f"{self.full_name} ({self.role})"
