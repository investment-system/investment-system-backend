from django.urls import path
from .views import AdminProfileView, AdminListView, AdminStatsView

urlpatterns = [

    path('admin/profile/', AdminProfileView.as_view(), name='admin-profile'),
    path('list/', AdminListView.as_view(), name='admin-list'),
    path('stats/', AdminStatsView.as_view(), name='admin-stats'),


]
