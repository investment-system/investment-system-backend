from rest_framework import serializers
from .models import CancellationRecord

class CancellationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancellationRecord
        fields = [
            'cancellation_code',
            'share',
            'cancellation_date',
            'payout_type',
            'penalty_rate',
            'penalty_amount',
            'refund_amount',
            'created_at'
        ]
        read_only_fields = ['cancellation_code', 'penalty_amount', 'refund_amount', 'created_at', 'cancellation_date']
