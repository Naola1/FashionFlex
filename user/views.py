from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

# Get the custom User model
User = get_user_model()

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)  # Authenticate using email
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Forgot password view
def forgot_password_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_user = User.objects.filter(email=email).first()
            if associated_user:
                subject = "Password Reset Requested"
                email_template_name = "password_reset_email.html"
                c = {
                    "email": associated_user.email,
                    "domain": request.META['HTTP_HOST'],
                    "site_name": "Your Site",
                    "uid": urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    "token": default_token_generator.make_token(associated_user),
                    "protocol": "http" if settings.DEBUG else "https",
                }
                email_content = render_to_string(email_template_name, c)
                send_mail(subject, email_content, settings.EMAIL_HOST_USER, [associated_user.email], fail_silently=False)
                messages.success(request, "A password reset link has been sent to your email.")
                return redirect("login")
            else:
                messages.error(request, "No user is associated with this email address.")
    else:
        form = PasswordResetForm()
    return render(request, "forgot_password.html", {"form": form})

# Reset password view
def reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect("login")
        else:
            form = SetPasswordForm(user)
    else:
        messages.error(request, "The reset password link is invalid, possibly because it has already been used.")
        return redirect("forgot_password")

    return render(request, "reset_password.html", {"form": form})
