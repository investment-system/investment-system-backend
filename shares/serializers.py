from rest_framework import serializers
from .models import Transaction
from shares.models import ShareRecord

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['transaction_code', 'created_at', 'transaction_id']

class ShareRecordSerializer(serializers.ModelSerializer):
    profit = serializers.SerializerMethodField()
    cancel = serializers.SerializerMethodField()

    class Meta:
        model = ShareRecord
        fields = [
            'share_id',
            'project_name',
            'share_date',
            'share_return_rate',
            'expected_share_maturity_date',
            'status',
            'share_duration_days',
            'invested_amount',
            'profit',
            'cancel'
        ]

    def get_profit(self, obj):
        if hasattr(obj, 'profitpayout'):
            from profits.serializers import ProfitPayoutSerializer
            return ProfitPayoutSerializer(obj.profitpayout).data
        return None

    def get_cancel(self, obj):
        cancel = obj.cancellationrecord_set.first()
        if cancel:
            from cancels.serializers import CancellationRecordSerializer
            return CancellationRecordSerializer(cancel).data
        return None
