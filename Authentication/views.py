from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.db import IntegrityError
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse
from django.conf import settings
import uuid

from .forms import PhoneSignUpForm, PhoneLoginForm, AdminLoginForm
from home.models import Profile

User = get_user_model()


def signup(request):
    """Simple phone number signup/login - Check if user exists, if not create, then login"""
    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER')
    if next_url and not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = None

    if request.method == 'POST':
        form = PhoneSignUpForm(request.POST)
        
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            # Check if user already exists with this phone number
            existing_user = User.objects.filter(phone_number=phone_number).first()
            
            if existing_user:
                # User exists, redirect to login
                messages.info(request, f"Account already exists with phone number {phone_number}. Please use the login option.")
                return redirect('phone_login')
            else:
                # Create new user
                try:
                    username = f"user_{uuid.uuid4().hex[:8]}"
                    user = User.objects.create_user(
                        username=username,
                        phone_number=phone_number,
                        first_name=first_name,
                        last_name=last_name,
                        is_phone_verified=True
                    )
                    
                    # Profile is created automatically by signal
                    # Update the phone number in the profile
                    user.profile.phone = str(phone_number)
                    user.profile.save()
                    
                    # Login user automatically
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    
                    messages.success(request, f"Welcome to ZENKO, {first_name}! Your account has been created.")
                    return redirect(next_url or 'home')
                    
                except IntegrityError as e:
                    # More specific error handling
                    messages.error(request, f"Account creation failed: {str(e)}. Please try again.")
                except Exception as e:
                    # Catch any other errors
                    messages.error(request, f"An error occurred: {str(e)}. Please try again.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PhoneSignUpForm()

    context = {'form': form}
    if next_url:
        context['next'] = next_url
    return render(request, 'signup.html', context)

def signin(request):
    """Main login page - shows options for phone or admin login"""
    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER')
    if next_url and not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = None

    context = {}
    if next_url:
        context['next'] = next_url
    return render(request, 'signin.html', context)

def phone_login(request):
    """Simple phone number login - Check if user exists and auto-login"""
    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER')
    if next_url and not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = None

    if request.method == 'POST':
        form = PhoneLoginForm(request.POST)
        
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            
            # Check if user exists with this phone number
            user = User.objects.filter(phone_number=phone_number).first()
            
            if user:
                # User exists, login automatically
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect(next_url or 'home')
            else:
                # User doesn't exist
                messages.error(request, f"No account found with phone number {phone_number}. Please sign up first.")
                return redirect('signup')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = PhoneLoginForm()

    context = {'form': form}
    if next_url:
        context['next'] = next_url
    return render(request, 'phone_login.html', context)

def admin_login(request):
    """Admin login with email and password"""
    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER')
    if next_url and not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = None

    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=email, password=password)
            
            if user is not None and user.is_superuser:
                # Login with standard backend
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f"Welcome back, Admin!")
                return redirect(next_url or '/admin/')
            else:
                messages.error(request, "Invalid admin credentials.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = AdminLoginForm()

    context = {'form': form}
    if next_url:
        context['next'] = next_url
    return render(request, 'admin_login.html', context)


def signout(request):
    # Support redirecting back to the page the user came from
    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER')
    if next_url and not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = None
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect(next_url or 'home')
