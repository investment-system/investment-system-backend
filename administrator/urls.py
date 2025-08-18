from django.urls import path
from .views import AdminProfileView, AdminListView, AdminStatsView, AdminDeleteView, AdminDetailView
urlpatterns = [

    path('profile/', AdminProfileView.as_view(), name='admin-profile'),
    path('<int:pk>/', AdminDetailView.as_view(), name='admin-detail'),
    path('<int:pk>/delete/', AdminDeleteView.as_view(), name='admin-delete'),
    path('list/', AdminListView.as_view(), name='admin-list'),
    path('stats/', AdminStatsView.as_view(), name='admin-stats'),
]

