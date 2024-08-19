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
    path('', homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('donor/', include('donor_management.urls')),
    path('project/', include('project_management.urls')),
    path('finance/', include('finance_management.urls')),

    # url for the elements of homepage and navbar
    path('login_as/', login_as_view, name='login_as'),
    path('signup_as/', signup_as_view, name='signup_as'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),

    #for admin
    path('admin_login/', admin_login, name='admin_login'),
    path('admin_signup/', admin_signup, name='admin_signup'),
    path('admin_home/', admin_home, name='admin_home'),
    path('pending_donations/', pending_donations, name='pending_donations'),
    path('accepted_donations/', accepted_donations, name='accepted_donations'),
    path('view_donation/<int:pid>/', view_donation, name='view_donation'),
    path('add_area/', add_donation_area, name='add_area'),
    path('manage_area/', manage_donation_area, name='manage_area'),
    path('edit_donation_area/<int:id>', edit_donation_area, name='edit_donation_area'),
    path('delete-area/<int:area_id>/', delete_area, name='delete_area'),
    path('manage_donors/', manage_donors, name='manage_donors'),
    path('view_donor_details/', view_donors_details, name='view_donors_details'),


    #For Volunteer 
    path('volunteer_signup/', volunteer_signup, name='volunteer_signup'),
    path('volunteer_login/', volunteer_login, name='volunteer_login'),

    #For Donor login and signup 
    path('donor_login/', donor_login, name='donor_login'),
    path('donor_signup/', donor_signup, name='donor_signup'),
    path('logout/', Logout, name='logout'),
]
