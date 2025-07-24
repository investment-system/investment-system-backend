from rest_framework import serializers
from .models import ProfitPayout

class ProfitPayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfitPayout
        fields = '__all__'
        read_only_fields = ['payout_id', 'profit_code', 'created_at']
