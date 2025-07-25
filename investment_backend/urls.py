from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Modular app routes
    path('api/transactions/', include('transactions.urls')),
    path('api/shares/', include('shares.urls')),
    path('api/profits/', include('profits.urls')),
    path('api/cancels/', include('cancels.urls')),
    path('api/registrations/', include('registrations.urls')),
    # path('api/members/', include('members.urls')),

]
#
# # Serve media files (profile pictures, etc.)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
