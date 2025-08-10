from django.urls import path
from .views import AdminRegisterView, AdminProfileView, AdminListView

urlpatterns = [
    path('register/', AdminRegisterView.as_view(), name='admin-register'),
    path('profile/', AdminProfileView.as_view(), name='admin-profile'),
    path('list/', AdminListView.as_view(), name='admin-list'),
]