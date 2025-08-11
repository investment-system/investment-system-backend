from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['transaction_code']

class TransactionStatsSerializer(serializers.Serializer):
    registration_amount = serializers.DecimalField(max_digits=15, decimal_places=2)

    share_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    share_completed = serializers.IntegerField()
    share_canceled = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_transactions = serializers.IntegerField()
    money_in = serializers.DecimalField(max_digits=15, decimal_places=2)
    money_out = serializers.DecimalField(max_digits=15, decimal_places=2)
    money_reinvest = serializers.DecimalField(max_digits=15, decimal_places=2)
    expected_profit = serializers.DecimalField(max_digits=15, decimal_places=2)
