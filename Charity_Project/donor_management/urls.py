# donor_management/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.donor_list, name='donor_list'),
    path('add/', views.add_donor, name='add_donor'),
    path('doner/<int:pk>/', views.donor_detail, name='donor_detail'),
    path('edit/<int:donor_id>/', views.edit_donor, name='donor_update'),
    path('delete/<int:donor_id>/', views.delete_donor, name='donor_delete'),
    # path('campaigns/', views.campaign_list_view, name='campaign_list'),
    path('donate_now/', views.donate_now, name='donate_now'),
    path('donor_home', views.donor_home, name='donor_home'),
    path('become_volunteer/', views.become_volunteer, name='become_volunteer'),
    path('donation_history', views.donation_history, name='donation_history')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)