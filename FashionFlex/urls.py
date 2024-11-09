from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", include('clothes.urls')),
    path("api/", include("shop.api.urls")),
    path("api/", include("user.api.urls")),
    path('api/cart/', include('cart.api.urls')),
]
