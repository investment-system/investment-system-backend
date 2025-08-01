from django.urls import path
from .views import (
    SignupView,
    ProfileView,
    ChangePasswordView,
    VerifyCodeView,
    ResendCodeView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="member-signup"),
    path("profile/", ProfileView.as_view(), name="member-profile"),
    path("change-password/", ChangePasswordView.as_view(), name="member-change-password"),
    path("verify-code/", VerifyCodeView.as_view(), name="verify-code"),
    path("resend-code/", ResendCodeView.as_view(), name="resend-code"),
]
