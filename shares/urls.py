from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShareRecordViewSet

router = DefaultRouter()
router.register(r'share-record', ShareRecordViewSet, basename='share')

urlpatterns = [
    path('', include(router.urls)),
]
