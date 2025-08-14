from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from members.models import Member

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'user_type', 'is_active']
        read_only_fields = ['id', 'is_active']

class BaseRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']
        extra_kwargs = {'full_name': {'required': True}}

    def create(self, validated_data):
        # This will be overridden by subclasses
        raise NotImplementedError()

class MemberRegisterSerializer(BaseRegisterSerializer):
    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password'],
            user_type='member'
        )

class AdminRegisterSerializer(BaseRegisterSerializer):
    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password'],
            user_type='admin',
            is_staff=True
        )

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

class MemberProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            'ic_number', 'gender', 'date_of_birth', 'phone_number',
            'country', 'city', 'state', 'bank_name',
            'account_holder_name', 'bank_account_number'
        ]

class UserWithMemberSerializer(serializers.ModelSerializer):
    member_profile = MemberProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'user_type', 'is_active',
            'member_profile'
        ]
        read_only_fields = ['id', 'is_active']