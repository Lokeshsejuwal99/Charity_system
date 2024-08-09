# donor_management/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.donor_list, name='donor_list'),
    path('add/', views.add_donor, name='add_donor'),
    path('doner/<int:pk>/', views.donor_detail, name='donor_detail'),
    path('edit/<int:donor_id>/', views.edit_donor, name='donor_update'),
    path('delete/<int:donor_id>/', views.delete_donor, name='donor_delete'),
]