from django.urls import path
from .views import RegisterView, LoginView, MeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='member-register'),
    path('login/', LoginView.as_view(), name='member-login'),
    path('me/', MeView.as_view(), name='member-me'),
]
