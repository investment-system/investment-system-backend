from django.contrib import admin
from .models import Administrator

@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('admin_code', 'user', 'role', 'position')
    list_filter = ('role', 'position')
    search_fields = ('admin_code', 'user__email', 'user__full_name')
    readonly_fields = ('created_at','updated_at','admin_code','user')
    raw_id_fields = ('user',)

    fieldsets = (
        (None, {'fields': ('user', 'admin_code')}),
        ('Personal Info', {'fields': (
            'gender', 'ic_number', 'date_of_birth', 'phone_number', 'profile_picture'
            ,'created_at','updated_at'
        )}),
        ('Admin Info', {'fields': ('role', 'position')}),
    )