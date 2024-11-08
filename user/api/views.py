from django.shortcuts import render
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,  
)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash

# Get the custom user model
User = get_user_model()

# API view for user registration
class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()

            if new_user:
                # Generate JWT tokens for the new user
                refresh = RefreshToken.for_user(new_user)
                access_token = str(refresh.access_token)
                
                response = Response({
                    'message': 'User registered successfully',
                    'user_id': new_user.id,
                    'email': new_user.email,
                    'access_token': access_token,
                    'refresh_token': str(refresh)
                }, status=status.HTTP_201_CREATED)
                return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view for user login    
class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        # Get email and password from the request data
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            # If either field is missing, return an error
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)

        if user is not None:
            # Generate JWT token for the authenticated user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'message': 'Login successful',
                'user_id': user.id,
                'email': user.email,
                'username': user.username,
                'access_token': access_token,
                'refresh_token': str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            # If authentication fails, return an error
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Blacklist the refresh token to log the user out
        refresh_token = serializer.validated_data.get('refresh_token')
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': 'Invalid token or token already blacklisted.'}, status=status.HTTP_400_BAD_REQUEST)

# # Pagination class for listing results with custom page sizes.
# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 100


# API view for changing password.
class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # Handle POST requests to change the user's password.
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        # Validate the serializer data
        if serializer.is_valid():
            user = request.user# Get the authenticated user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
