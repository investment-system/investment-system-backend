from shares.serializers import ShareRecordSerializer
from rest_framework import serializers
from .models import Transaction
from members.models import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name', 'email', 'phone']  # only the fields you need

class TransactionSerializer(serializers.ModelSerializer):
    share_record = ShareRecordSerializer(read_only=True, allow_null=True)  # allow null

    class Meta:
        model = Transaction
        fields = '__all__'

class TransactionStatsSerializer(serializers.Serializer):
    registration_amount = serializers.DecimalField(max_digits=15, decimal_places=2)

    share_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    share_completed = serializers.IntegerField()
    share_canceled = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_transactions = serializers.IntegerField()
    money_in = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_balance = serializers.DecimalField(max_digits=15, decimal_places=2)
    money_out = serializers.DecimalField(max_digits=15, decimal_places=2)
    money_reinvest = serializers.DecimalField(max_digits=15, decimal_places=2)
    expected_profit = serializers.DecimalField(max_digits=15, decimal_places=2)
