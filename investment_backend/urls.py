from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('transactions.urls')),
    path('api/', include('shares.urls')),
    path('api/', include('profits.urls')),
    path('api/', include('cancels.urls')),
]

