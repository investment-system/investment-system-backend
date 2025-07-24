# cancels/admin.py
from django.contrib import admin
from .models import CancellationRecord

@admin.register(CancellationRecord)
class CancellationRecordAdmin(admin.ModelAdmin):
    list_display = ['cancellation_code', 'share', 'penalty_rate', 'penalty_amount', 'refund_amount', 'cancellation_date']
    readonly_fields = ['penalty_amount', 'refund_amount', 'cancellation_code']  # Optional: to make them read-only
