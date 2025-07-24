from rest_framework import serializers
from .models import RegistrationPayment
from transactions.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'transaction_code', 'member_id', 'amount', 'payment_method', 'created_at']

class RegistrationPaymentSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer(read_only=True)

    class Meta:
        model = RegistrationPayment
        fields = ['payment_id', 'member_id', 'transaction', 'payment_code', 'confirmed_at', 'created_at']
