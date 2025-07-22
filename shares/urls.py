from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShareRecordViewSet

router = DefaultRouter()
router.register(r'share-records', ShareRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
