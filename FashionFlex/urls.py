from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", include('clothes.urls')),
    path("api/", include("shop.api.urls")),
    path("api/", include("user.api.urls")),
    path('api/cart/', include('cart.api.urls')),
    path('', include('shop.urls')),

    path("__reload__/", include("django_browser_reload.urls")),
]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)