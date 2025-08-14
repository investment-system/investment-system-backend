from rest_framework import serializers
from .models import Member

class MemberListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    full_name = serializers.CharField(source='user.full_name')

    class Meta:
        model = Member
        fields = ['member_code', 'full_name', 'email', 'gender', 'registration_status', 'created_at']

class MemberProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = Member
        fields = [
            'email', 'full_name', 'member_code', 'gender', 'ic_number', 'date_of_birth',
            'phone_number', 'country', 'address_line', 'city', 'state',
            'bank_name', 'account_holder_name', 'bank_account_number',
            'profile_picture', 'registration_status'
        ]
        read_only_fields = ['member_code']

class MemberRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    gender = serializers.ChoiceField(choices=Member.GENDER_CHOICES)

    def create(self, validated_data):
        user_data = {
            'email': validated_data['email'],
            'full_name': validated_data['full_name'],
            'password': validated_data['password'],
            'user_type': 'member'
        }

        member_data = {
            'gender': validated_data['gender']
        }

        # This would be handled in the view
        return {'user_data': user_data, 'member_data': member_data}

class VerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

class MemberStatsSerializer(serializers.Serializer):
    total_members = serializers.IntegerField()
    total_active_members = serializers.IntegerField()
    total_inactive_members = serializers.IntegerField()
