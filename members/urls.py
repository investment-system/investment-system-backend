from django.urls import path
from .views import (
    MemberLoginView,
    SignupView,
    MemberListView,
    MemberDetailView,
    ProfileView,
    ChangePasswordView,
    VerifyCodeView,
    ResendCodeView,
    RequestPasswordResetView,
    ResetPasswordView,
)
urlpatterns = [

    path('signup/', SignupView.as_view(), name='member-signup'),
    path('login/', MemberLoginView.as_view(), name='member-login'),
    path('profile/', ProfileView.as_view(), name='member-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('resend-code/', ResendCodeView.as_view(), name='resend-code'),
    path('request-reset-password/', RequestPasswordResetView.as_view(), name='request-reset-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),


    path('members/', MemberListView.as_view(), name='member-list'),
    path('members/<int:pk>/', MemberDetailView.as_view(), name='member-detail'),
]
