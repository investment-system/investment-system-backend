from django.urls import path
from .views import (
    MemberLoginView,
    SignupView,
    MemberListView,
    MemberDetailView,
    VerifyCodeView,
    ResendCodeView,
    ActivateAccountView,
    ProfileView,
    ChangePasswordView
)

urlpatterns = [
    path("members/", MemberListView.as_view(), name="member-list"),
    path("members/<int:pk>/", MemberDetailView.as_view(), name="member-detail"),
    path("members/signup/", SignupView.as_view(), name="member-signup"),
    path("members/login/", MemberLoginView.as_view(), name="member-login"),
    path("members/profile/", ProfileView.as_view(), name="member-profile"),
    path("members/change-password/", ChangePasswordView.as_view(), name="change-password"),
]
