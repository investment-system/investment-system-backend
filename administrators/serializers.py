from rest_framework import serializers
from .models import Administrator
from django.contrib.auth import authenticate


class AdminRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Administrator
        fields = ['email', 'full_name', 'password']
        extra_kwargs = {
            'full_name': {'required': False, 'allow_blank': True}
        }

    def create(self, validated_data):
        return Administrator.objects.create_user(**validated_data)


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = [
            'admin_code', 'email', 'full_name', 'ic_number', 'gender',
            'date_of_birth', 'phone_number', 'profile_picture',
            'role', 'position'
        ]
        read_only_fields = ['admin_code', 'email']


class AdminPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
