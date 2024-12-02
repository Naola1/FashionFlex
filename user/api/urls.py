from django.urls import path, include
from .views import (
	UserRegistrationAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
	# UserProfileView,
    # DoctorListAPIView,
    # DoctorDetailAPIView,
    ChangePasswordView    
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
   # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationAPIView.as_view(), name='api-register'),
    path('login/', UserLoginAPIView.as_view(), name='api-login'),
    path('logout/', UserLogoutAPIView.as_view(), name='api-logout'),
# 	path('user/profile/', UserProfileView.as_view(), name='user-profile'),
#     path('doctors/', DoctorListAPIView.as_view(), name='doctor-list'),
#     path('doctors/<int:id>/', DoctorDetailAPIView.as_view(), name='doctor-detail'),
    path('change-password/', ChangePasswordView.as_view(), name='api-change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='api-password_reset')),
]