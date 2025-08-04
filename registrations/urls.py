from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistrationPaymentViewSet

router = DefaultRouter()
router.register(r'registrations', RegistrationPaymentViewSet, basename='registration')

urlpatterns = [
    path('', include(router.urls)),
]
