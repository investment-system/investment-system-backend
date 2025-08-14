from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .models import Administrator
from rest_framework import serializers


User = get_user_model()

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

class AdminStatsSerializer(serializers.Serializer):
    total_admins = serializers.IntegerField()
    active_admins = serializers.IntegerField()
    inactive_admins = serializers.IntegerField()

class AdminStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total = User.objects.filter(user_type='admin').count()
        active = User.objects.filter(user_type='admin', is_active=True).count()
        inactive = User.objects.filter(user_type='admin', is_active=False).count()

        data = {
            'total_admins': total,
            'active_admins': active,
            'inactive_admins': inactive
        }

        serializer = AdminStatsSerializer(data)
        return Response(serializer.data)