from django.urls import path
from .views import (
    MemberRegisterView,
    AdminRegisterView,
    ChangePasswordView,
    UserProfileView,
    AdminListView,
    MemberListView,
    MyTokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('member/register/', MemberRegisterView.as_view(), name='member-register'),
    path('admin/register/', AdminRegisterView.as_view(), name='admin-register'),

    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/', UserProfileView.as_view(), name='profile'),

    path('administrators/', AdminListView.as_view(), name='admin-list'),
    path('members/', MemberListView.as_view(), name='member-list'),

]
