# In your view where donation is processed
from finance_management.models import Budget
from donor_management.models import Donor, Donation
from project_management.models import Project
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DonorForm


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



def donor_list(request):
    donors = Donor.objects.all()
    return render(request, 'donor_management/donor_list.html', {'donors': donors})

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
    return render(request, 'donor_management/donate_now.html')

def become_volunteer(request):
    return render(request, 'donor_management/become_volunteer.html')