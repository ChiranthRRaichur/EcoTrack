from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('waste.urls')),  # End users urls
     path('admin-portal/', include('admin_app.urls')),  # Admin portal URLs
]

# Serve media files during development
if settings.DEBUG:  # Ensure this only applies during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
