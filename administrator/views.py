from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from authentication.models import User
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .models import Administrator

User = get_user_model()

class AdminRegisterView(APIView):
    permission_classes = [IsAdminUser]  # Only existing admins can register new admins

    def post(self, request):
        serializer = AdminRegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Create user
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                full_name=serializer.validated_data['full_name'],
                password=serializer.validated_data['password'],
                user_type='admin',
                is_staff=True
            )

            # Create admin profile
            admin = Administrator.objects.create(
                user=user,
                role=serializer.validated_data['role']
            )

            return Response({
                'message': 'Admin registration successful'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminListView(generics.ListAPIView):
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Administrator.objects.all()

class AdminProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type != 'admin':
            return Response({'detail': 'Not an admin user'}, status=status.HTTP_403_FORBIDDEN)
        try:
            admin_profile = Administrator.objects.get(user=user)
        except Administrator.DoesNotExist:
            return Response({'detail': 'Admin profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdministratorSerializer(admin_profile)
        return Response(serializer.data)
