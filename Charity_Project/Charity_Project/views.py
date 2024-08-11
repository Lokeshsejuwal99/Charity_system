from django.shortcuts import render

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