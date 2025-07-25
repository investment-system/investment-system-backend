from django.urls import path
from .views import (
    AdminRegisterView,
    AdminLoginView,
    AdminProfileView,
    AdminPasswordChangeView
)

urlpatterns = [
    path('register/', AdminRegisterView.as_view(), name='admin-register'),
    path('login/', AdminLoginView.as_view(), name='admin-login'),
    path('profile/', AdminProfileView.as_view(), name='admin-profile'),
    path('change-password/', AdminPasswordChangeView.as_view(), name='admin-change-password'),
]
