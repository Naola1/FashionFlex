from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Get the custom User model
User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password']  # Use fields from your custom User model

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, label="Email")  # Use email as the login field
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
