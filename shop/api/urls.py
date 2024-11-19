from django.urls import path
from .views import HomeListAPIView, DetailAPIView

urlpatterns = [
    path("home/", HomeListAPIView.as_view(), name="api-home"),
    path('cloth/<int:cloth_id>/', DetailAPIView.as_view(), name='api-cloth-detail'),
]
