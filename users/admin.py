from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'role', 'is_active', 'created_at')
    search_fields = ('email', 'full_name', 'ic_number')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
            'fields': (
                'full_name', 'ic_number', 'gender', 'date_of_birth',
                'phone_number', 'profile_picture', 'email_verified',
                'verification_token'
            )
        }),
        ('Address & Bank Info', {
            'fields': (
                'country', 'address_line', 'city', 'state',
                'bank_name', 'account_holder_name', 'bank_account_number'
            )
        }),
        ('Roles & Status', {
            'fields': (
                'role', 'position', 'is_active', 'is_staff', 'is_superuser',
                'last_login', 'activated_at'
            )
        }),
        ('Permissions', {
            'fields': ('groups', 'user_permissions')
        }),
    )
