from rest_framework import serializers
from .models import Administrator
from authentication.serializers import UserSerializer

class AdminProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Administrator
        fields = [
            'user', 'admin_code', 'gender', 'ic_number', 'date_of_birth',
            'phone_number', 'profile_picture', 'role', 'position'
        ]
        read_only_fields = ['admin_code']

class AdminRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=Administrator.ROLE_CHOICES, default='admin')

    def create(self, validated_data):
        user_data = {
            'email': validated_data['email'],
            'full_name': validated_data['full_name'],
            'password': validated_data['password'],
            'user_type': 'admin',
            'is_staff': True  # All admins are staff by default
        }

        admin_data = {
            'role': validated_data['role']
        }

        return {'user_data': user_data, 'admin_data': admin_data}