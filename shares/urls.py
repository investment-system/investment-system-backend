from rest_framework.routers import DefaultRouter
from .views import ShareRecordViewSet

router = DefaultRouter()
router.register(r'share', ShareRecordViewSet, basename='share')


urlpatterns = router.urls

