from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('home', views.home_view, name='home'),
    path('cloth/<int:cloth_id>/', views.cloth_detail_view, name='cloth_detail'),
    path('rented/', views.rented_view, name='rented_list'),
]
