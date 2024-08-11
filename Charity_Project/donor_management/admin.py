from django.contrib import admin
from .models import Donation, Donor, Volunteer, DonationArea, Gallery

# Register your models here.
admin.site.register(Donor)
admin.site.register(Donation)
admin.site.register(DonationArea)
admin.site.register(Volunteer)
admin.site.register(Gallery)

