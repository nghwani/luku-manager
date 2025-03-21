# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
import random
from .models import User, PhoneVerification
from .forms import UserRegistrationForm, LoginForm

class EmailVerificationMixin:
    @staticmethod
    def send_verification_email(request, user, email):
        token = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request)
        subject = 'Verify your email address'
        
        message = render_to_string('authentication/email/verify_email.html', {
            'user': user,
            'domain': current_site.domain,
            'token': token,
        })
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User won't be able to login until verified
            user.save()
            
            # Send verification email
            EmailVerificationMixin.send_verification_email(request, user, form.cleaned_data['email'])
            
            # Generate and send phone verification code
            verification = PhoneVerification.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                code=str(random.randint(100000, 999999))
            )
            # In production, use a proper SMS service here
            print(f"Verification code: {verification.code}")  # For development
            
            messages.success(request, 'Please check your email and phone for verification.')
            return redirect('verify_phone')
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})

def verify_email(request, token):
    try:
        uid = force_str(urlsafe_base64_decode(token))
        user = User.objects.get(pk=uid)
        
        if not user.is_active:
            user.email_verified = True
            if user.phone_verified:  # If phone is also verified
                user.is_active = True
            user.save()
            messages.success(request, 'Email verified successfully!')
        return redirect('login')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Invalid verification link')
        return redirect('register')

def verify_phone(request):
    if request.method == 'POST':
        code = request.POST.get('verification_code')
        try:
            verification = PhoneVerification.objects.get(
                code=code,
                is_verified=False
            )
            user = verification.user
            user.phone_verified = True
            if user.email_verified:  # If email is also verified
                user.is_active = True
            user.save()
            
            verification.is_verified = True
            verification.save()
            
            messages.success(request, 'Phone number verified successfully!')
            return redirect('login')
        except PhoneVerification.DoesNotExist:
            messages.error(request, 'Invalid verification code')
    return render(request, 'authentication/phone/verify_phone.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Please verify your email and phone number.')
            else:
                messages.warning(request, 'Invalid username or password.')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

