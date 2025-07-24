from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfitPayoutViewSet

router = DefaultRouter()
router.register(r'profit-payouts', ProfitPayoutViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
