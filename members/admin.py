from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member

@admin.register(Member)
class MemberAdmin(UserAdmin):
    model = Member

    list_display = (
        'email', 'member_code', 'full_name', 'gender',
        'phone_number', 'country', 'is_staff', 'is_active',
        'created_at', 'updated_at',
    )
    list_filter = ('is_staff', 'is_active', 'gender', 'country', 'state')
    ordering = ('-created_at',)
    search_fields = ('email', 'full_name', 'member_code', 'phone_number', 'ic_number')

    readonly_fields = ('member_code', 'created_at', 'updated_at', 'date_joined')

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': (
                'member_code', 'full_name', 'gender', 'ic_number', 'date_of_birth',
                'phone_number', 'profile_picture',
            )
        }),
        ('Address Info', {
            'fields': (
                'country', 'address_line', 'city', 'state',
            )
        }),
        ('Bank Info', {
            'fields': (
                'bank_name', 'account_holder_name', 'bank_account_number',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
        ('Timestamps', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'full_name', 'password1', 'password2',
                'is_staff', 'is_active',
            ),
        }),
    )
