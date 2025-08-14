from django.contrib import admin
from .models import RegistrationPayment

@admin.register(RegistrationPayment)
class RegistrationPaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'transaction', 'member_id', 'confirmed_at', 'created_at']
    readonly_fields = ['created_at',]
