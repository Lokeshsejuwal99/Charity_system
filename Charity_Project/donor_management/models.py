from django.db import models
from django.contrib.auth.models import User
from datetime import timezone

class Campaign(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('inactive', 'Inactive'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_raised = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def is_active(self):
        return self.status == 'active' and self.start_date <= timezone.now() <= self.end_date
    

    @property
    def progress_percentage(self):
        if self.goal_amount > 0:
            return (self.amount_raised / self.goal_amount) * 100
        return 0
    

class Donor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    amount_donated = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='donors', null=True)
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
    profile_pic = models.ImageField(null=True)
    contact = models.CharField(max_length=40, null=True)
    address = models.CharField(max_length=40, null=True)
    aboutme = models.CharField(max_length=400, null=True)
    status = models.CharField(max_length=30, choices=Volunteer_status, null=True)
    identity_card = models.FileField(null=True)
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
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    donation_name = models.CharField(max_length=300, null=True)
    donation_pic = models.FileField(null=True)
    amount = models.CharField(max_length=30, null=True)
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
    user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"Donation of {self.amount} by {self.donor.user.first_name}"
    

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


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


