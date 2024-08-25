from django.contrib import admin
from .models import Donation, Donor, Volunteer, DonationArea, ContactMessage, Request_for_donation, Donation_Gallery

# Register your models here.
admin.site.register(Donor)
admin.site.register(Donation)
admin.site.register(DonationArea)
admin.site.register(Volunteer)
admin.site.register(ContactMessage)
admin.site.register(Donation_Gallery)
admin.site.register(Request_for_donation)
