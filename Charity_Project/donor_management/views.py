# In your view where donation is processed
from finance_management.models import Budget
from donor_management.models import Donor, Donation
from project_management.models import Project
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DonorForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from donor_management.models import Donor
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def process_donation(donor_id, amount, project_id=None):
    donor = Donor.objects.get(id=donor_id)
    project = Project.objects.get(id=project_id) if project_id else None

    # Create the Donation record
    donation = Donation.objects.create(
        donor=donor,
        campaign=None,
        amount=amount,
        payment_method='esewa',
        transaction_id='TRANSACTION1234',
        status='success'
    )

    # Update the Budget record
    budget, created = Budget.objects.get_or_create(donor=donor, project=project, defaults={
        'total_budget': 0,
        'remaining_budget': 0,
    })

    budget.total_budget += amount
    budget.update_budget(amount)

    return donation

def donor_home(request):
    if not request.user.is_authenticated:
        return redirect('donor_login')
    return render(request, 'donor_management/donor_home.html')  

def donation_history(request):
    if not request.user.is_authenticated:
        return redirect('donor_login')

    user = request.user
    donor = Donor.objects.get(user=user)
    donations = Donation.objects.filter(donor=donor).order_by('-created_at')

    return render(request, 'donor_management/donation_history.html', {'donations': donations})


def add_donor(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('donor_list')
    else:
        form = DonorForm()
    return render(request, 'donor_management/add_donor.html', {'form': form})

def edit_donor(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    if request.method == 'POST':
        form = DonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            return redirect('donor_list')
    else:
        form = DonorForm(instance=donor)
    return render(request, 'donor_management/edit_donor.html', {'form': form})

def delete_donor(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    if request.method == 'POST':
        donor.delete()
        return redirect('donor_list')
    return render(request, 'donor_management/delete_doner.html', {'donor': donor})


def donor_detail(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    return render(request, 'donor_management/doner_detail.html', {'donor': donor})

def donate_now(request):
    if not request.user.is_authenticated:
        return redirect('donor_login')
    
    user = request.user
    donor = Donor.objects.get(user=user)
    error = None  # Default to no error

    if request.method == 'POST':
        try:
            donationname = request.POST.get('donation_name')
            donationpic = request.FILES.get('donation_pic')
            collectionloc = request.POST.get('collection_loc')
            description = request.POST.get('description')

            if not all([donationname, collectionloc, description]):
                raise ValueError("All required fields must be filled")

            Donation.objects.create(
                donor=donor,
                donation_name=donationname,
                donation_pic=donationpic,
                collection_loc=collectionloc,
                description=description,
                status='pending'
            )
            messages.success(request, "Collection request has been submitted. We will contact you soon.")
            return redirect('donation_history')
        except Exception as e:
            print(f"Error occurred: {e}")
            messages.error(request, 'An error occurred while submitting the donation.')
            return redirect('donate_now')

    return render(request, 'donor_management/donate_now.html', {'error': error})

def become_volunteer(request):
    return render(request, 'donor_management/become_volunteer.html')

