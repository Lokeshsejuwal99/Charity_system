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
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('donor/', include('donor_management.urls')),
    path('project/', include('project_management.urls')),
    path('finance/', include('finance_management.urls')),

    # url for the elements of homepage and navbar
    path('login_as/', login_as_view, name='login_as'),
    path('gallery/', donation_gallery, name='donation_gallery'),
    path('signup_as/', signup_as_view, name='signup_as'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('feedback/', feedback_page, name='feedback_page'),

    # For request for donation
    path('request_for_donation/', request_for_donation, name='request_for_donation'),
    path('thank-you/', thank_you, name='thank_you'),

    # For campaign management
    path('campaigns/', campaign_list, name='campaign_list'),
    path('campaigns/new/', create_campaign, name='create_campaign'),
    path('active_campaign/', active_campaign, name='active_campaign'),
    path('campaigns/<int:campaign_id>/donate/', DonateView, name='donate'),
    path('campaigns/<int:campaign_id>/', campaign_detail, name='campaign_detail'),
    path('campaign_learn_more/<int:campaign_id>/', campaign_learn_more, name='campaign_learn_more'),
    path('campaigns/<int:campaign_id>/edit/', update_campaign, name='update_campaign'),
    path('campaigns/<int:campaign_id>/delete/', delete_campaign, name='delete_campaign'),


    #for admin
    path('admin_login/', admin_login, name='admin_login'),
    path('admin_signup/', admin_signup, name='admin_signup'),
    path('admin_home/', admin_dashboard, name='admin_home'),
    path('inquires/', inquires_view, name='inquires'),
    path('inquiries/message/<int:message_id>/', view_message_details, name='view_message_details'),
    path('admin_feedbacks/', feedback_list_admin, name='feedback_list_admin'),
    path('admin_feedbacks/<int:feedback_id>/', view_feedback, name='view_feedback'),
    path('admin_feedbacks/<int:feedback_id>/delete/', delete_feedback, name='delete_feedback'),
    path('pending_donations/', pending_donations, name='pending_donations'),
    path('accepted_donations/', accepted_donations, name='accepted_donations'),
    path('view_donation/<int:pid>/', view_donation, name='view_donation'),
    path('accepted_donation_details/<int:pid>/', accepted_donation_details, name='accepted_donation_details'),
    path('guest-donations/', guest_donations, name='guest_donations'),
    path('add_area/', add_donation_area, name='add_area'),
    path('manage_area/', manage_donation_area, name='manage_area'),
    path('edit_donation_area/<int:id>/', edit_donation_area, name='edit_donation_area'),
    path('delete_area/<int:area_id>/', delete_area, name='delete_area'),
    path('manage_donors/', manage_donors, name='manage_donors'),
    path('view_donor_details/<int:id>/', view_donors_details, name='view_donors_details'),
    path('delete_donors/<int:donor_id>/', delete_donors, name='delete_donors'),
    path('donation_requests_view/', donation_requests_view, name='donation_requests_view'),
    path('donation_requests/<int:id>/', donation_requests_details_view, name='donation_request_detail'),

    #For Volunteer 
    path('volunteer_signup/', volunteer_signup, name='volunteer_signup'),
    path('volunteer_login/', volunteer_login, name='volunteer_login'),
    path('volunteer_base/', volunteer_base, name='volunteer_base'),
    path('Volunteer_home/', Volunteer_home, name='Volunteer_home'),
    path('profile_volunteer', profile_volunteer, name='profile_volunteer'),
    path('active_campaign_volunteer/', active_campaign_volunteer, name='active_campaign_volunteer'),
    path('volunteer_requests/', volunteer_requests, name='volunteer_requests'),
    path('accepted_volunteer/', accepted_volunteer, name='accepted_volunteer'),
    path('rejected_volunteer/', rejected_volunteer, name='rejected_volunteer'),
    path('all_volunteer/', all_volunteer, name='all_volunteer'),
    path('view_volunteer_details/<int:id>/', view_volunteer_details, name='view_volunteer_details'),
    path('edit_volunteer/', edit_volunteer_profile, name='edit_volunteer_profile'),
    path('delete_volunteer/<int:id>/', delete_volunteer, name='delete_volunteer'),
    path('collection_req', donation_collection_requests, name='collection_req'),
    path('collection_req_details/<int:id>/', collection_req_details, name='collection_req_details'),
    path('donation_receive', donation_received, name='donation_receive'),
    path('donation_not_received/', donation_not_received, name='donation_not_received'),
    path('donation_rec_details/<int:id>', donation_rec_details, name='donation_rec_details'),
    path('donation_delivered/', donation_delivered, name='donation_delivered'),
    path('donation_delivered_details/<int:id>/', donation_delivered_details, name='donation_delivered_details'),



    #For Donor login and signup 
    path('donor_login/', donor_login, name='donor_login'),
    path('donor_signup/', donor_signup, name='donor_signup'),
    path('logout/', Logout, name='logout'),



    #For esewa integration
    path('payment/<int:id>/', initiate_payment, name='initiate_payment'),
    path('success/', payment_success, name='esewa_success'),
    path('failure/', payment_failure, name='esewa_failure'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)