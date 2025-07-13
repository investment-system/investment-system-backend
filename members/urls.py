# member/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),  # Matches /api/member/
]
