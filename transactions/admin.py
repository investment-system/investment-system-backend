from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_code', 'source_type', 'direction', 'amount', 'member_id']
    readonly_fields = ['transaction_code', 'created_at']

