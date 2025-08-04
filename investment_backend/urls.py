from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Modular app routes
    path('api/', include('transactions.urls')),
    path('api/', include('shares.urls')),
    path('api/', include('profits.urls')),
    path('api/', include('cancels.urls')),
    path('api/', include('registrations.urls')),
    path('api/', include('administrators.urls')),
    path('api/', include('members.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
