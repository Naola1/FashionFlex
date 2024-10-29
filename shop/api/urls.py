from django.urls import path
from .views import HomeListAPIView, DetailAPIView

urlpatterns = [
    path("home/", HomeListAPIView.as_view(), name="home"),
    path('cloth/<int:cloth_id>/', DetailAPIView.as_view(), name='cloth-detail'),
]
