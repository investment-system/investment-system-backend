from rest_framework import serializers
from .models import CancellationRecord
from shares.models import ShareRecord
from .models import CancellationRecord

class CancellationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancellationRecord
        fields = [
            'cancelled_share_id',
            'share_record',
            'cancellation_reason',
            'refund_transaction',
            'cancelled_at'
        ]
        read_only_fields = ['cancelled_share_id', 'cancelled_at']
