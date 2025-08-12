from django.urls import path
from .views import (
    MemberProfileView,
    MemberListView,
    MemberStatsAPIView,
)

urlpatterns = [
    path('list/', MemberListView.as_view(), name='members-list'),
    path('profile/', MemberProfileView.as_view(), name='member-profile'),
    path('stats/', MemberStatsAPIView.as_view(), name='member-stats'),

]
