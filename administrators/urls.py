from django.urls import path
from .views import (
    AdminRegisterView,
    AdminLoginView,
    AdminProfileView,
    AdminPasswordChangeView
)

urlpatterns = [
    path('administrator/register/', AdminRegisterView.as_view(), name='admin-register'),
    path('administrator/login/', AdminLoginView.as_view(), name='admin-login'),
    path('administrator/profile/', AdminProfileView.as_view(), name='admin-profile'),
    path('administrator/change-password/', AdminPasswordChangeView.as_view(), name='admin-change-password'),
]
