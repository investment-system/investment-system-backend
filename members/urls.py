from django.urls import path
from .views import (
    MemberRegisterView,
    VerifyMemberView,
    MemberProfileView,
    MemberListView
)

urlpatterns = [
    path('members/', MemberListView.as_view(), name='members-list'),
    path('register/', MemberRegisterView.as_view(), name='member-register'),
    path('verify/', VerifyMemberView.as_view(), name='member-verify'),
    path('profile/', MemberProfileView.as_view(), name='member-profile'),
]
