from django.urls import path
from .views import HomeListAPIView, DetailAPIView

urlpatterns = [
    path('home/',HomeListAPIView.as_view() , name='home'),
    path('detail/',DetailAPIView.as_view(), name='detail'),
]