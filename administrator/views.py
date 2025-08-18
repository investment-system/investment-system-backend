from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import Administrator
from .serializers import AdminProfileSerializer


User = get_user_model()

class AdminListView(generics.ListAPIView):
    serializer_class = AdminProfileSerializer  # include full profile
    permission_classes = [IsAuthenticated]
    queryset = Administrator.objects.select_related('user').all()

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

    def patch(self, request):
        """Partial update of admin profile"""
        user = request.user
        if user.user_type != 'admin':
            return Response({'detail': 'Not an admin user'}, status=status.HTTP_403_FORBIDDEN)
        try:
            admin_profile = Administrator.objects.get(user=user)
        except Administrator.DoesNotExist:
            return Response({'detail': 'Admin profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdministratorSerializer(admin_profile, data=request.data, partial=True)  # ✅ partial=True
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminDeleteView(APIView):
    permission_classes = [IsAdminUser]  # Only admins can delete

    def delete(self, request, pk):
        try:
            admin = Administrator.objects.get(pk=pk)
            admin.user.delete()  # optionally delete the related user too
            admin.delete()
            return Response({'detail': 'Admin deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Administrator.DoesNotExist:
            return Response({'detail': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

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

class AdminDetailView(generics.RetrieveAPIView):
    queryset = Administrator.objects.select_related('user')
    serializer_class = AdminDetailSerializer
    permission_classes = [IsAuthenticated]