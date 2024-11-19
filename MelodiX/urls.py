from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# Custom error handlers
from melodixapp.views import custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('', lambda request: redirect('login')),  # Redirect root to login
    path('', include('melodixapp.urls')),  # Include app-specific URLs
]

# Serve media and static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handler
handler404 = 'melodixapp.views.custom_404_view'
