from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import (
    UserSerializer,
    MemberRegisterSerializer,
    MemberLoginSerializer,
    AdminRegisterSerializer,
    AdminLoginSerializer,
    ChangePasswordSerializer
)
from .models import User

# Member views
class MemberRegisterView(generics.CreateAPIView):
    serializer_class = MemberRegisterSerializer
    permission_classes = [permissions.AllowAny]

class MemberLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = MemberLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })

# Admin views
class AdminRegisterView(generics.CreateAPIView):
    serializer_class = AdminRegisterSerializer
    permission_classes = [permissions.IsAdminUser]  # Only existing admins can register new admins

class AdminLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })

# Shared views
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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