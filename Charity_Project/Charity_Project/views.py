from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.middleware.csrf import get_token
from donor_management.models import Donor

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

def donor_login(request):
    return render(request, 'donor_login.html')

def volunteer_login(request):
    return render(request, 'volunteer_login.html')

def signup_as_view(request):
   return render(request, 'signup_as.html')

def admin_signup(request):
    return render(request, 'admin_signup.html')


def donor_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        district = request.POST.get('district')
        country = request.POST.get('country')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('donor_signup')

        # Additional validation (if needed)
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('donor_signup')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('donor_signup')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('donor_signup')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Create the Donor associated with the user
        donor = Donor.objects.create(
            user=user,
            phone_number=phone_number,
            address=address,
            district=district,
            country=country
        )
        donor.save()

        # Log the user in after successful signup
        login(request, user)
        messages.success(request, "Signup successful. You are now logged in.")
        return redirect('donor_login')

    return render(request, 'donor_signup.html')


    return render(request, 'donor_signup.html')
def volunteer_signup(request):
    return render(request, 'volunteer_signup.html')