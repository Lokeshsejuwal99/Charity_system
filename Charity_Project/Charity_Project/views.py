from django.shortcuts import render

def homepage(request):
 return render(request, 'homepage.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def about_view(request):
 return render(request, 'about.html')

def contact_view(request):
 return render(request, 'contact.html')
