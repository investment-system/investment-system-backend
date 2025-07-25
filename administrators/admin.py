from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Administrator

@admin.register(Administrator)
class AdministratorAdmin(UserAdmin):
    model = Administrator
    list_display = ('admin_code', 'email', 'full_name', 'role', 'position', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'role', 'position')
    search_fields = ('email', 'admin_code', 'full_name', 'ic_number', 'phone_number')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('admin_code', 'email', 'password')}),
        ('Personal Info', {
            'fields': (
                'full_name', 'ic_number', 'gender', 'date_of_birth', 'phone_number', 'profile_picture', 'role', 'position'
            )
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    readonly_fields = ('admin_code', 'created_at', 'updated_at', 'last_login')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'full_name', 'ic_number', 'gender', 'date_of_birth',
                'phone_number', 'profile_picture', 'role', 'position',
                'password1', 'password2', 'is_staff', 'is_active'
            ),
        }),
    )
