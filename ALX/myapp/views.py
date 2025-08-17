from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('home')
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Musique

# Create your views here.

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})



from django.contrib.auth.decorators import login_required
from django.db import models

@login_required(login_url='register')
def list_musique(request):
    user = request.user
    musiques = Musique.objects.filter(
        models.Q(publique=True) |
        models.Q(utilisateurs_autorises=user)
    ).distinct()
    return render(request, 'listMusique.html', {'musiques': musiques})