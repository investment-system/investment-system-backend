from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Modular app routes
    path('api/transactions/', include('transactions.urls')),
    path('api/shares/', include('shares.urls')),
    path('api/profits/', include('profits.urls')),
    path('api/cancels/', include('cancels.urls')),
    path('api/registrations/', include('registrations.urls')),
    path('api/admin/', include('administrators.urls')),
    path('api/members/', include('members.urls')),

]