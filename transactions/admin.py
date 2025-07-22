from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'source_type', 'direction', 'amount', 'payment_method', 'created_at')
    list_filter = ('source_type', 'direction', 'payment_method')
    search_fields = ('transaction_id', 'reference_id')
