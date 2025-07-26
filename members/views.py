from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Member
from .serializers import (
    MemberSignupSerializer,
    MemberProfileSerializer,
    ChangePasswordSerializer
)
from rest_framework.permissions import IsAuthenticated


class SignupView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSignupSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = MemberProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    queryset = Member.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        member = self.request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not member.check_password(serializer.validated_data.get("old_password")):
                return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            member.set_password(serializer.validated_data.get("new_password"))
            member.save()

            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
