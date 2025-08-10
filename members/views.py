from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.utils import timezone
from django.contrib.auth import get_user_model
from authentication.models import User
from .serializers import *
from authentication.utils import send_verification_email
from .models import Member

User = get_user_model()


class MemberListView(generics.ListAPIView):
    queryset = Member.objects.select_related('user').all().order_by('-created_at')
    serializer_class = MemberListSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__email', 'user__full_name', 'member_code']
    ordering_fields = ['created_at', 'member_code']


class MemberRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MemberRegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Create user
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                full_name=serializer.validated_data['full_name'],
                password=serializer.validated_data['password'],
                user_type='member',
                is_active=False  # Require verification
            )

            # Create member profile
            member = Member.objects.create(
                user=user,
                gender=serializer.validated_data['gender']
            )

            # Generate and send verification code
            member.generate_verification_code()
            send_verification_email(user, member.verification_code)

            return Response({
                'message': 'Registration successful. Please check your email for verification code.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyMemberView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'], user_type='member')
                member = Member.objects.get(user=user)

                if member.verification_code != serializer.validated_data['code']:
                    return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

                if timezone.now() - member.code_created_at > timezone.timedelta(minutes=10):
                    return Response({'error': 'Verification code expired'}, status=status.HTTP_400_BAD_REQUEST)

                user.is_active = True
                user.save()
                member.verification_code = None
                member.code_created_at = None
                member.save()

                return Response({'message': 'Account verified successfully'})

            except (User.DoesNotExist, Member.DoesNotExist):
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemberProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = MemberProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Member.objects.get(user=self.request.user)