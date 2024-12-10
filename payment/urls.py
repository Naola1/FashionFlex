# from django.urls import path
# from . import views

# urlpatterns = [
#     path('initiate/<int:cloth_id>/', views.initiate_payment, name='initiate_payment'),
#     path('success/', views.payment_success, name='payment_success'),
#     path('cancel/', views.payment_cancel, name='payment_cancel'),
#     # path('webhook/', views.stripe_webhook, name='stripe_webhook'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('initiate/', views.initiate_payment, name='initiate_payment'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    # path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]