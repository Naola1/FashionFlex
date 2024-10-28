from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    #path("", include('clothes.urls')),
    path("api/", include('clothes.api.urls')),
]