from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),

    # Modular app routes
    path('api/transactions/', include('transactions.urls')),
    path('api/', include('registrations.urls')),
    path('api/share/', include('shares.urls')),
    path('api/', include('profits.urls')),

    path('api/auth/', include('authentication.urls')),
    path('api/members/', include('members.urls')),
    path('api/administrators/', include('administrator.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
