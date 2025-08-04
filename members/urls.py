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
)
urlpatterns = [

    path('member/signup/', SignupView.as_view(), name='member-signup'),
    path('member/login/', MemberLoginView.as_view(), name='member-login'),
    path('member/profile/', ProfileView.as_view(), name='member-profile'),
    path('member/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('member/verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('member/resend-code/', ResendCodeView.as_view(), name='resend-code'),

    path('members/', MemberListView.as_view(), name='member-list'),
    path('members/<int:pk>/', MemberDetailView.as_view(), name='member-detail'),
]
