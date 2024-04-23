# views.py
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def home(request):
    return render(request, 'home.html', {'year': 2024})  # You can pass any context data you need here


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
    else:
        profile_form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'profile_form': profile_form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse('profile'))  # Redirect to 'profile' URL name
    else:
        profile_form = UserProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'profile_form': profile_form})


