from django.contrib import admin
from .models import Donation, Donor, DonationReceipt, Campaign

# Register your models here.
admin.site.register(Campaign)
admin.site.register(Donor)
admin.site.register(Donation)
admin.site.register(DonationReceipt)
