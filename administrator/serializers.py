from rest_framework import serializers
from .models import Administrator
from authentication.serializers import UserSerializer
from authentication.models import User

class AdministratorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', required=False)
    full_name = serializers.CharField(source='user.full_name', required=False)

    class Meta:
        model = Administrator
        fields = '__all__'
        extra_kwargs = {
            'gender': {'required': False},
            'ic_number': {'required': False},
            'date_of_birth': {'required': False},
            'phone_number': {'required': False},
            'profile_picture': {'required': False},
            'role': {'required': False},
            'position': {'required': False},
        }

    def update(self, instance, validated_data):
        # Handle nested User updates
        user_data = validated_data.pop('user', {})
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()

        # Update Administrator fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'user_type', 'is_active', 'date_joined']

class AdminDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Administrator
        fields = '__all__'

