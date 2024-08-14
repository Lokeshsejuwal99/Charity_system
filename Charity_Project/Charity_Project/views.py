from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.middleware.csrf import get_token
from donor_management.models import Donor
from django.contrib.auth import login, logout, authenticate

def homepage(request):
 return render(request, 'homepage.html')

def about_view(request):
 return render(request, 'about.html')

def contact_view(request):
 return render(request, 'contact.html')

# For login and signup 

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def login_as_view(request):
    return render(request, 'login_as.html')

def admin_login(request):
    return render(request, 'admin_login.html')

def volunteer_signup(request):
    return render(request, 'volunteer_signup.html')

def volunteer_login(request):
    return render(request, 'volunteer_login.html')

def signup_as_view(request):
   return render(request, 'signup_as.html')

def admin_signup(request):
    return render(request, 'admin_signup.html')