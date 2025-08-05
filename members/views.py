from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Content
from .models import Member
from .serializers import (
    MemberSignupSerializer,
    MemberProfileSerializer,
    ChangePasswordSerializer
)

class MemberListView(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberProfileSerializer
    permission_classes = [AllowAny]

class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberProfileSerializer
    permission_classes = [AllowAny]

class SignupView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSignupSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        user.generate_verification_code()

        subject = "Verify Your Account"
        html_content = f"""
            Hi {user.full_name or user.email},<br><br>
            Your verification code is: <strong>{user.verification_code}</strong><br>
            This code expires in 10 minutes.
        """

        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=user.email,
            subject=subject,
            html_content=html_content
        )

        sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        sg.send(message)

class MemberLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"detail": "Email and password required."}, status=400)

        try:
            user = Member.objects.get(email=email)
        except Member.DoesNotExist:
            return Response({"detail": "Invalid email or password."}, status=401)

        user = authenticate(request, username=user.username, password=password)

        if not user:
            return Response({"detail": "Invalid email or password."}, status=401)

        if not user.is_active:
            return Response({"detail": "Account not activated."}, status=403)

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
            from_email=Email(settings.DEFAULT_FROM_EMAIL),
            to_emails=Email(user.email),
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

class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email is required."}, status=400)

        try:
            user = Member.objects.get(email=email)
        except Member.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        user.generate_verification_code()

        message = Mail(
            from_email=Email(settings.DEFAULT_FROM_EMAIL),
            to_emails=Email(user.email),
            subject="Reset Your Password",
            html_content=f"""
                Hi {user.full_name or user.email},<br><br>
                Use the following code to reset your password:<br><br>
                <strong>{user.verification_code}</strong><br><br>
                This code will expire in 10 minutes.
            """
        )

        sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        sg.send(message)

        return Response({"detail": "Password reset code sent to email."}, status=200)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not all([email, code, new_password, confirm_password]):
            return Response({"detail": "All fields are required."}, status=400)

        if new_password != confirm_password:
            return Response({"detail": "Passwords do not match."}, status=400)

        try:
            user = Member.objects.get(email=email)
        except Member.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        if user.verification_code != code:
            return Response({"detail": "Invalid verification code."}, status=400)

        if timezone.now() - user.code_created_at > timezone.timedelta(minutes=10):
            return Response({"detail": "Code expired."}, status=400)

        user.set_password(new_password)
        user.verification_code = None
        user.code_created_at = None
        user.save()

        return Response({"detail": "Password reset successful."}, status=200)

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
                return Response({"detail": "Old password is incorrect."}, status=400)

            member.set_password(serializer.validated_data.get("new_password"))
            member.save()
            return Response({"detail": "Password changed successfully."}, status=200)

        return Response(serializer.errors, status=400)
