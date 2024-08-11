"""
URL configuration for Charity_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('doner/', include('donor_management.urls')),
    path('project/', include('project_management.urls')),
    path('finance/', include('finance_management.urls')),

    # url for the elements of homepage and navbar
    path('', homepage, name='homepage'),
    path('login_as/', login_as_view, name='login_as'),
    path('signup/', signup_view, name='signup'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),

    #for admin, volunteer and doner login
    path('admin_login/', admin_login, name='admin_login'),
    path('donor_login/', donor_login, name='donor_login'),
    path('volunteer_login/', volunteer_login, name='volunteer_login'),

]
