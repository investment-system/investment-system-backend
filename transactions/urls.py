from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, TransactionStatsAPIView

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),  # Matches /transactions/ etc.
    path('stats/', TransactionStatsAPIView.as_view(), name='transaction-stats'),  # Matches /stats/
]
