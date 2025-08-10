from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'member_code', 'user', 'gender', 'registration_status',
        'masked_ic_number', 'masked_bank_account'
    )
    list_filter = ('gender', 'registration_status')
    search_fields = ('member_code', 'user__email', 'user__full_name')
    readonly_fields = ['member_code', 'created_at', 'updated_at']
    raw_id_fields = ('user',)

    # Full fieldsets (for superusers)
    base_fieldsets = (
        (None, {'fields': ('user', 'member_code')}),
        ('Personal Info', {'fields': (
            'gender', 'ic_number', 'date_of_birth', 'phone_number',
            'country', 'address_line', 'city', 'state'
        )}),
        ('Bank Info', {'fields': (
            'bank_name', 'account_holder_name', 'bank_account_number'
        )}),
        ('Other', {'fields': (
            'profile_picture', 'registration_status'
        )}),
    )

    # Limited fieldsets (for non-superusers)
    restricted_fieldsets = (
        (None, {'fields': ('user', 'member_code')}),
        ('Personal Info', {'fields': (
            'gender', 'country'
        )}),
        ('Other', {'fields': (
            'profile_picture', 'registration_status'
        )}),
    )

    def get_fieldsets(self, request, obj=None):
        """Show limited fields if user is not a superuser."""
        if request.user.is_superuser:
            return self.base_fieldsets
        return self.restricted_fieldsets

    def get_readonly_fields(self, request, obj=None):
        """Make sensitive fields read-only for non-superusers (if visible)."""
        if request.user.is_superuser:
            return self.readonly_fields
        return self.readonly_fields + [
            'ic_number', 'date_of_birth', 'phone_number',
            'address_line', 'city', 'state',
            'bank_name', 'account_holder_name', 'bank_account_number'
        ]

    # Masked display for sensitive fields in list view
    def masked_ic_number(self, obj):
        if not obj.ic_number:
            return "-"
        return f"****{obj.ic_number[-4:]}" if len(obj.ic_number) >= 4 else "****"
    masked_ic_number.short_description = "IC Number"

    def masked_bank_account(self, obj):
        if not obj.bank_account_number:
            return "-"
        return f"****{obj.bank_account_number[-4:]}" if len(obj.bank_account_number) >= 4 else "****"
    masked_bank_account.short_description = "Bank Account"
