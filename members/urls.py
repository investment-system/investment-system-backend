from django.urls import path
from .views import SignupView, ProfileView, ChangePasswordView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="member-signup"),
    path("profile/", ProfileView.as_view(), name="member-profile"),
    path("change-password/", ChangePasswordView.as_view(), name="member-change-password"),
]
