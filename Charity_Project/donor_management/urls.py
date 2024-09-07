# donor_management/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('add/', views.add_donor, name='add_donor'),
    # path('campaigns/', views.campaign_list_view, name='campaign_list'),
    path('donate_now/', views.donate_now, name='donate_now'),
    path('donor_home', views.donor_home, name='donor_home'),
    path('become_volunteer/', views.become_volunteer, name='become_volunteer'),
    path('donation_history', views.donation_history, name='donation_history'),
    path('profile_donor', views.profile_donor, name='profile_donor'),
    path('donation/<int:donation_id>/delete/', views.delete_donation, name='delete_donation'),
    path('donation/<int:donation_id>/edit/', views.edit_donation, name='donation_edit'),
    path('edit-profile/', views.edit_donor_profile, name='edit_donor_profile'),
    path('donation/donor/<int:donation_id>/', views.donor_view_donation, name='donor_view_donation'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)