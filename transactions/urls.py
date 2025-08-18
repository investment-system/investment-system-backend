from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TransactionViewSet,
    TransactionStatsAPIView,
    UserTransactionDetailAPIView,
    UserTransactionsAPIView,
    AdminMemberTransactionListAPIView,
)

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserTransactionsAPIView.as_view(), name='user-transactions'),
    path('user/<int:pk>/', UserTransactionDetailAPIView.as_view(), name='user-transaction-detail'),
    path('stats/', TransactionStatsAPIView.as_view(), name='transaction-stats'),
    path('admin/member/<int:member_id>/transactions/', AdminMemberTransactionListAPIView.as_view(), name='admin-member-transactions'),

]
