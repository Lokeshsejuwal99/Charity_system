# In your view where donation is processed
from donor_management.models import Donor, Donation
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DonorForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from donor_management.models import Donor
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum


def donor_home(request):
    # Get the Donor instance associated with the logged-in user
    donor = get_object_or_404(Donor, user=request.user)

    # Calculate the total donations
    total_donations = Donation.objects.filter(donor=donor).count()

    # Get recent donations (e.g., last 5)
    recent_donations = Donation.objects.filter(donor=donor).order_by('-created_at')[:]

    context = {
        'total_donations': total_donations,
        'recent_donations': recent_donations,
    }

    return render(request, 'donor_management/donor_home.html', context)

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


@login_required
def profile_donor(request):
    try:
        donor = Donor.objects.get(user=request.user)
    except Donor.DoesNotExist:
        messages.error(request, "Donor profile not found.")
        return redirect('donor_signup')  # Or a relevant page

    if request.method == 'POST':
        # Handle profile update logic if necessary
        pass

    context = {
        'donor': donor,
    }
    return render(request, 'profile_donor.html', context)

@login_required
def edit_donor_profile(request):
    donor = get_object_or_404(Donor, user=request.user)

    if request.method == 'POST':
        # Update user details
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')  # Ensure email is included
        user.save()

        # Update donor details
        donor.phone_number = request.POST.get('phone_number')
        donor.address = request.POST.get('address')
        donor.district = request.POST.get('district')
        donor.country = request.POST.get('country')
        donor.save()

        return redirect('profile_donor')
    
    context = {
        'donor': donor,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,  # Include email in context
        'phone_number': donor.phone_number,
        'address': donor.address,
        'district': donor.district,
        'country': donor.country
    }

    return render(request, 'profile_donor_edit.html', context)



@login_required
def delete_donation(request, donation_id):
    # Get the donation object by ID and delete it
    donation = get_object_or_404(Donation, id=donation_id)
    donation.delete()
    # Redirect to the donation history page after deletion
    return redirect('donation_history') 



@login_required
def edit_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    
    if request.method == 'POST':
        donation.donation_name = request.POST.get('donation_name')
        donation.description = request.POST.get('description')
        donation.collection_loc = request.POST.get('collection_loc')
        donation.donation_pic = request.FILES.get('donation_pic')
        donation.save()
        return redirect('donation_history')  # Replace with the correct URL name

    context = {
        'donation': donation
    }   
    return render(request, 'donor_management/edit_donation.html', context)


def donor_view_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)

    context = {
        'donation': donation
    }
    return render(request, 'donor_management/view_donation_details.html', context)