from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Member


class MemberSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    member_code = serializers.CharField(read_only=True)

    class Meta:
        model = Member
        fields = ['email', 'full_name', 'password', 'member_code']

    def create(self, validated_data):
        return Member.objects.create_user(**validated_data)


class MemberProfileSerializer(serializers.ModelSerializer):
    member_code = serializers.CharField(read_only=True)

    class Meta:
        model = Member
        fields = [
            'email', 'full_name', 'phone_number', 'member_code',
            'ic_number', 'gender', 'date_of_birth',
            'country', 'address_line', 'city', 'state',
            'bank_name', 'account_holder_name', 'bank_account_number',
            'profile_picture',
        ]



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New password and confirm password do not match.")
        return data
