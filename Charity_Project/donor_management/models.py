from django.db import models
from django.contrib.auth.models import User

class Donor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username if self.user else "No Username"

class Volunteer(models.Model):
    Volunteer_status = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('inactive', 'Inactive')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=40, null=True)
    address = models.CharField(max_length=40, null=True)
    aboutme = models.CharField(max_length=400, null=True)
    status = models.CharField(max_length=30, choices=Volunteer_status, null=True)
    admin_remarks = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.username

class DonationArea(models.Model):
    area_name = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.area_name
    
class Donation(models.Model):

    STATUS_CHOICES = [
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('failed', 'Failed')
    ]

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    donation_name = models.CharField(max_length=300, null=True)
    donation_pic = models.FileField(null=True)
    collection_loc = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=500, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_remarks = models.CharField(max_length=500, null=True)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True)
    volunteer_remarks = models.CharField(max_length=500, null=True)
    donation_area = models.ForeignKey(DonationArea, on_delete=models.CASCADE, null=True)
    donation_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.donation_name


class Request_for_donation(models.Model):
    name = models.CharField(max_length=100)
    contact_no = models.IntegerField()
    request_for = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Donation_Gallery(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    delivery_pic     = models.FileField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.donation.donation_name
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"