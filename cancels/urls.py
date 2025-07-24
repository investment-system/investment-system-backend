from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CancellationRecordViewSet

router = DefaultRouter()
router.register(r'cancellation-record', CancellationRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
