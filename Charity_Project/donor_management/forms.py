from django import forms
from .models import Donor, Campaign

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['phone_number', 'address', 'district', 'country']


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'goal_amount', 'start_date', 'end_date', 'status']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }