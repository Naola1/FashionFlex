from rest_framework import serializers
from django.contrib.auth import get_user_model
from user.models import User


User = get_user_model()
# Serializer for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']  
    # Overriding the create method to handle role-based profile creation
    def create(self, validated_data):
        
        user = self.Meta.model(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
#Serializer for user login       
class UserLoginSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=100)
	username = serializers.CharField(max_length=100, read_only=True)
	password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
	token = serializers.CharField(max_length=255, read_only=True)
     
class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
# Serializer for Reset password Email
class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
# Serializer for email verification
# class EmailVerificationSerializer(serializers.ModelSerializer):
#     token = serializers.CharField(max_length=555)

#     class Meta:
#         model = get_user_model()
#         fields = ['token']

# # Serializer for detailed user information
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'middle_name', 'last_name', 
#                   'gender', 'date_of_birth', 'phone_number', 'address', 
#                   'emergency_contact_name', 'emergency_contact_number', 'role']
#         read_only_fields = ['email', 'username']  
#     # Overriding the update method for partial updates
#     def update(self, instance, validated_data):
        
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance
# # Serializer for DoctorProfile
# class DoctorProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = DoctorProfile
#         fields = ['id', 'user', 'specialization', 'bio', 'profile_picture', 
#                   'experience', 'qualification']
#     # Overriding the update method for nested updates (user and doctor data)
#     def update(self, instance, validated_data):
#         user_data = validated_data.pop('user', {})
#         user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
#         user_serializer.is_valid(raise_exception=True)
#         user_serializer.save()

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance
# # Serializer for PatientProfile
# class PatientProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = PatientProfile
#         fields = ['user', 'medical_history', 'allergies']
#     # Overriding the update method for nested updates
#     def update(self, instance, validated_data):
#         user_data = validated_data.pop('user', {})
#         user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
#         user_serializer.is_valid(raise_exception=True)
#         user_serializer.save()

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance
# # Serializer for ReceptionistProfile
# class ReceptionistProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = ReceptionistProfile
#         fields = ['user']
#     # Overriding the update method for nested updates
#     def update(self, instance, validated_data):
#         user_data = validated_data.pop('user', {})
#         user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
#         user_serializer.is_valid(raise_exception=True)
#         user_serializer.save()

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance
    
# # Serializer for Change password
# class ChangePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)
# # Serializer for Reset password Email
# class ResetPasswordEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)