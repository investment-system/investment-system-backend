from django.contrib import admin
from .models import ProfitPayout

@admin.register(ProfitPayout)
class ProfitPayoutAdmin(admin.ModelAdmin):
    list_display = [
        'payout_id',
        'payout_type',
        'get_original_amount',
        'payout_type',
        'profit_rate',
        'profit_amount',
        'refund_amount',
        'created_at',
    ]

    readonly_fields = [
        'get_original_amount',
        'profit_rate',
        'profit_amount',
        'refund_amount',
        'created_at',
    ]

    def get_original_amount(self, obj):
        return f"{obj.original_amount:.2f} RM" if obj.original_amount else "0.00 RM"
    get_original_amount.short_description = 'Original Amount'
