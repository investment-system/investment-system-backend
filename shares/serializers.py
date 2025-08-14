from rest_framework import serializers
from .models import Transaction
from shares.models import ShareRecord


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['transaction_code', 'created_at', 'transaction_id']

class ShareRecordSerializer(serializers.ModelSerializer):
    received_transaction = TransactionSerializer()

    class Meta:
        model = ShareRecord
        fields = '__all__'

    def create(self, validated_data):
        transaction_data = validated_data.pop('received_transaction')
        transaction = Transaction.objects.create(**transaction_data)
        share_record = ShareRecord.objects.create(received_transaction=transaction, **validated_data)
        return share_record
