from django.urls import path
from .views import (
    MemberRegisterView,
    MemberLoginView,
    AdminRegisterView,
    AdminLoginView,
    LogoutView,
    ChangePasswordView,
    UserProfileView,
    AdminListView,
    MemberListView
)

urlpatterns = [

    # Member endpoints
    path('member/register/', MemberRegisterView.as_view(), name='member-register'),
    path('member/login/', MemberLoginView.as_view(), name='member-login'),

    # Admin endpoints
    path('admin/register/', AdminRegisterView.as_view(), name='admin-register'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),

    # Shared endpoints
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('administrators/', AdminListView.as_view(), name='admin-list'),
    path('members/', MemberListView.as_view(), name='member-list'),


]