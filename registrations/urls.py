from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistrationPaymentViewSet

router = DefaultRouter()
router.register(r'registration-payments', RegistrationPaymentViewSet, basename='registration-payment')

urlpatterns = [
    path('', include(router.urls)),
]
