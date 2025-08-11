from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import *
from members.models import Member

User = get_user_model()

class MemberListView(generics.ListAPIView):
    queryset = Member.objects.select_related('user').all().order_by('-created_at')
    serializer_class = MemberListSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__email', 'user__full_name', 'member_code']
    ordering_fields = ['created_at', 'member_code']

class MemberProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = MemberProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Member.objects.get(user=self.request.user)

class MemberStatsAPIView(APIView):
    def get(self, request):
        total_members = Member.objects.count()
        total_active_members = Member.objects.filter(registration_status='paid').count()
        total_inactive_members = Member.objects.filter(registration_status='unpaid').count()

        data = {
            "total_members": total_members,
            "total_active_members": total_active_members,
            "total_inactive_members": total_inactive_members,
        }

        serializer = MemberStatsSerializer(data=data)
        serializer.is_valid()

        return Response(serializer.data)
