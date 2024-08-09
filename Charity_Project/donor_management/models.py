from django.db import models

class Campaign(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('inactive', 'Inactive')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=20, decimal_places=2)
    amount_raised = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Donor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Donation(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('esewa', 'eSewa'),
        ('paypal', 'PayPal'),
        ('card', 'Credit/Debit Card')
    ]

    STATUS_CHOICES = [
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('failed', 'Failed')
    ]

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    donation_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Donation of {self.amount} by {self.donor} to {self.campaign if self.campaign else 'General Fund'}"


class DonationReceipt(models.Model):
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=100, unique=True)
    receipt_pdf = models.FileField(upload_to='receipts/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt {self.receipt_number} for {self.donation}"
