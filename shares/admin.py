from django.contrib import admin
from .models import ShareRecord

@admin.register(ShareRecord)
class ShareRecordAdmin(admin.ModelAdmin):
    list_display = [
        'share_id',
        'project_name',
        'status',
        'member_id',
        'share_date',
        'expected_share_maturity_date',
        'profit_amount',
        'received_transaction',
    ]
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['status', 'project_name']
    search_fields = ['member_id', 'project_name']

    def profit_amount(self, obj):
        return obj.calculate_profit()

    profit_amount.short_description = 'Profit Amount'
