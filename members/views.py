from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.utils import timezone
import sendgrid
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator


from sendgrid.helpers.mail import Mail
from .models import Member
from .serializers import (
    MemberSignupSerializer,
    MemberProfileSerializer,
    ChangePasswordSerializer
)
from .utils import generate_activation_link, decode_uid

class MemberListView(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberProfileSerializer
    permission_classes = [AllowAny]

class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberProfileSerializer
    permission_classes = [AllowAny]  # or IsAdminUser or custom permissions

class SignupView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSignupSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)

class MemberLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"detail": "Email and password required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Member.objects.get(email=email)
        except Member.DoesNotExist:
            return Response({"detail": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(request, username=user.username, password=password)

        if not user:
            return Response({"detail": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"detail": "Account not activated."}, status=status.HTTP_403_FORBIDDEN)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.id})

class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        if not email or not code:
            return Response({"detail": "Email and code are required."}, status=400)

        try:
            user = Member.objects.get(email=email)
        except Member.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        if user.verification_code != code:
            return Response({"detail": "Invalid code."}, status=400)

        if timezone.now() - user.code_created_at > timezone.timedelta(minutes=10):
            return Response({"detail": "Code has expired."}, status=400)

        user.is_active = True
        user.verification_code = None
        user.code_created_at = None
        user.save()

        return Response({"detail": "Account verified and activated successfully."}, status=200)

class ResendCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email is required."}, status=400)

        try:
            user = Member.objects.get(email=email)
        except Member.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        if user.is_active:
            return Response({"detail": "Account already activated."}, status=400)

        user.generate_verification_code()

        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=user.email,
            subject="Your New Verification Code",
            html_content=f"""
                Hi {user.full_name or user.email},<br><br>
                Your new verification code is: <strong>{user.verification_code}</strong><br>
                This code expires in 10 minutes.<br>
            """
        )
        sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        sg.send(message)

        return Response({"detail": "Verification code resent."})

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = decode_uid(uidb64)
            user = Member.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Member.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("Account activated successfully! You can now log in.")
        else:
            return HttpResponse("Activation link is invalid or expired.")

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
