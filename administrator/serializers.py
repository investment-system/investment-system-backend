from rest_framework import serializers
from .models import Administrator
from authentication.serializers import UserSerializer

class AdministratorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Administrator
        fields = '__all__'

class AdminListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    full_name = serializers.CharField(source='user.full_name')

    class Meta:
        model = Administrator
        fields = ['id', 'full_name', 'email', 'role', 'created_at']

class AdminProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Administrator
        fields = [
            'user', 'admin_code', 'gender', 'ic_number', 'date_of_birth',
            'phone_number', 'profile_picture', 'role', 'position'
        ]
        read_only_fields = ['admin_code']

class AdminStatsSerializer(serializers.Serializer):
    total_admins = serializers.IntegerField()
    active_admins = serializers.IntegerField()
    inactive_admins = serializers.IntegerField()
