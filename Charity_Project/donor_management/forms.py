from django import forms
from .models import Donor

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['user', 'phone_number', 'address', 'district', 'country']
