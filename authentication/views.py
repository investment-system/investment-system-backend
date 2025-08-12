from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .serializers import (
    UserSerializer,
    MemberRegisterSerializer,
    AdminRegisterSerializer,
    ChangePasswordSerializer
)
from .models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD  # tells parent to use 'email' instead of 'username'

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['user_type'] = user.user_type
        return token

    def validate(self, attrs):
        user = authenticate(email=attrs.get('email'), password=attrs.get('password'))
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("Account disabled")

        # Now parent validate expects 'email', not 'username'
        data = super().validate(attrs)
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'user_type': user.user_type,
        }
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class MemberRegisterView(generics.CreateAPIView):
    serializer_class = MemberRegisterSerializer
    permission_classes = [permissions.AllowAny]

class AdminRegisterView(generics.CreateAPIView):
    serializer_class = AdminRegisterSerializer
    permission_classes = [permissions.IsAdminUser]

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'status': 'password changed'})

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class AdminListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(user_type='admin')

class MemberListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(user_type='member')
