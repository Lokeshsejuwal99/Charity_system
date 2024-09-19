from donor_management.models import (Donor, Donation, DonationArea, Volunteer, ContactMessage, 
                                     Donation_Gallery, Request_for_donation, Feedback, Campaign)
from donor_management.forms import CampaignForm, DonorForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.middleware.csrf import get_token
from django.contrib.auth import login, logout, authenticate
from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views import View
import uuid
from django.http import HttpResponse

import base64
import json
from decimal import Decimal

def homepage(request):
    campaigns = Campaign.objects.filter(status='active')

    context = {
        'campaigns': campaigns
    }
    return render(request, 'homepage.html', context)


def donation_gallery(request):
    gallery_items = Donation_Gallery.objects.all().order_by('-created_at')
    return render(request, 'gallery.html', {'gallery_items': gallery_items})

def about_view(request):
 return render(request, 'about.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        ContactMessage.objects.create(name=name, email=email, message=message)
        
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return render(request, 'contact.html')


def feedback_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save feedback
        Feedback.objects.create(name=name, email=email, message=message)

        return redirect('feedback_page')  # Redirect to the same page after submitting feedback

    # Fetch recent feedbacks
    recent_feedbacks = Feedback.objects.all().order_by('-created_at')[:10]

    context = {
        'recent_feedbacks': recent_feedbacks
    }

    return render(request, 'feedback_page.html', context)

# For login and signup 

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def login_as_view(request):
    return render(request, 'login_as.html')

def signup_as_view(request):
   return render(request, 'signup_as.html')



# Needy People request for donation 
def request_for_donation(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact_no = request.POST.get('contact_no')
        request_for = request.POST.get('request_for')

        # Save the data to the model
        Request_for_donation.objects.create(
            name=name,
            contact_no=contact_no,
            request_for=request_for
        )

        return redirect('thank_you')

    return render(request, 'request_donation.html')


def thank_you(request):
    return render(request, 'thankyou.html')


# Donor login and signup credentials 
def donor_login(request):
    error = None
    if request.method == 'POST':
        email = request.POST['email_id']
        pwd = request.POST['password']
        user = authenticate(username=email, password=pwd)
        if user:
            login(request, user)
            return redirect('donor_home')
        else:
            error = "yes"
    return render(request, 'donor_login.html', {'error': error})

def donor_signup(request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email_id']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        district = request.POST.get('district')
        country = request.POST.get('country')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('donor_signup')

        # Additional validation (if needed)
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('donor_signup')

        # Check if the username already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Username already taken.")
            return redirect('donor_signup')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('donor_signup')

        # Create the user
        user = User.objects.create_user(username=email, email=email, password=password, first_name=firstname, last_name=lastname)
        user.save()

        # Create the Donor associated with the user
        donor = Donor.objects.create(
            user=user,
            phone_number=phone_number,
            address=address,
            district=district,
            country=country
        )
        donor.save()

        # Log the user in after successful signup
        login(request, user)
        messages.success(request, "Signup successful. You are now logged in.")
        return redirect('donor_login')

    return render(request, 'donor_signup.html')



"""Admin View"""

# For admin credentials and permissions

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=username, password=pwd)
        if user.is_staff:
            login(request, user)
            error = "no"
        else:
            error = "yes"
    return render(request, 'admin_login.html', locals())


def admin_dashboard(request):
    total_donors = Donor.objects.count()
    total_campaigns = Campaign.objects.count()
    total_donations = Donation.objects.count()
    active_volunteers = Volunteer.objects.filter(status='active').count()

    context = {
        'total_donors': total_donors,
        'total_campaigns': total_campaigns,
        'total_donations': total_donations,
        'active_volunteers': active_volunteers,
        'user': request.user
    }

    return render(request, 'admin_home.html', context)

def pending_donations(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donations = Donation.objects.filter(status='pending')
    return render(request, 'pending_donation.html', locals())


def accepted_donations(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to your admin login if needed
    
    donations = Donation.objects.filter(status='accept')  # Registered donors
    return render(request, 'accepted_donations.html', {'donations': donations})



def guest_donations(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to your admin login if needed
    
    donations = Donation.objects.filter(status='accept', user__isnull=True)  # Guest donors
    return render(request, 'campaign/guest_donations.html', {'donations': donations})


def view_donation(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donation = Donation.objects.get(id=pid)

    if request.method == "POST":
        status = request.POST['status']
        adminremark = request.POST['adminremark']

        try:
            donation.status = status
            donation.admin_remarks = adminremark
            donation.updated_at = date.today()
            donation.save()

            return render(request, 'view_donation.html', {'donation': donation, 'error': 'no'})
        except Exception as e:
            return render(request, 'view_donation.html', {'donation': donation, 'error': 'yes'})
    else:
        return render(request, 'view_donation.html', {'donation': donation})


def accepted_donation_details(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donation = Donation.objects.get(id=pid)
    volunteer = Volunteer.objects.all()
    donationarea = DonationArea.objects.all()

    if request.method == "POST":
        donationareaid = request.POST['donationareaid']
        volunteerid = request.POST['volunteerid']
        da = DonationArea.objects.get(id=donationareaid)
        v = Volunteer.objects.get(id=volunteerid)

        try:
            donation.donation_area = da
            donation.volunteer = v
            donation.status = "Volunteer Allocated"
            donation.updated_at = date.today()
            donation.save()

            return render(request, 'accepted_donations_details.html', locals())
        except Exception as e:
            return render(request, 'accepted_donations_details.html', locals())
    else:
        return render(request, 'accepted_donations_details.html', locals())



def add_donation_area(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    if request.method == "POST":
        areaname = request.POST['areaname']
        description = request.POST['description']
        try:
            DonationArea.objects.create(area_name=areaname, description=description)
            error = "no"
        except:
            error = "yes"

    return render(request, 'add_area.html', locals())



def manage_donation_area(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    area = DonationArea.objects.all()
    return render(request, 'manage_area.html',  locals())


def edit_donation_area(request, id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    area = DonationArea.objects.get(id=id)
    if request.method == "POST":
        areaname = request.POST['areaname']
        description = request.POST['description']
        area.area_name = areaname
        area.description = description
        try:
            area.save()
            error = "no"
        except:
            error = "yes"

    return render(request, 'edit_donation_area.html', locals())

@login_required
def delete_area(request, area_id):
    DonationArea.objects.get(id=area_id).delete()
    return redirect('manage_area')
    
@login_required
def manage_donors(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donors = Donor.objects.all()
    return render(request, 'manage_donors.html',  locals())

@login_required
def view_donors_details(request, id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    donors = Donor.objects.get(id=id)
    return render(request, 'view_donors_details.html', locals())

@login_required
def delete_donors(request, donor_id):
    Donor.objects.get(id=donor_id).delete()
    return redirect('manage_donors')


@login_required
def inquires_view(request):
    messages = ContactMessage.objects.all()
    return render(request, 'inquires.html', {'messages': messages})

@login_required
def view_message_details(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    return render(request, 'inquires_details.html', {'message': message})

@login_required
def feedback_list_admin(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'feedback_list_admin.html', {'feedbacks': feedbacks})


@login_required
def view_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    return render(request, 'view_feedback.html', {'feedback': feedback})

@require_http_methods(["DELETE"])
@login_required
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.user.is_staff:
        feedback.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=403)


@login_required
def donation_requests_view(request):
    request_donation = Request_for_donation.objects.all()
    return render(request, 'request_donation_admin_site.html', locals())

@login_required
def donation_requests_details_view(request, id):
    request_donation = get_object_or_404(Request_for_donation, id=id)
    return render(request, 'donation_requests_details_view.html', {'request': request_donation})
















# For Volunteers 
def volunteer_signup(request):
    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email_id')
        contact = request.POST.get('phone_number')
        address = request.POST.get('address')
        aboutme = request.POST.get('aboutme')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('volunteer_signup')

        # Check if password length is sufficient
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('volunteer_signup')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('volunteer_signup')

        # Create the user
        user = User.objects.create_user(username=email, email=email, password=password, first_name=firstname, last_name=lastname)
        user.save()

        # Create the Volunteer associated with the user
        Volunteer.objects.create(
            user=user,
            contact=contact,
            address=address,
            aboutme=aboutme,
            status='pending',
            profile_pic=request.FILES.get('profile_pic'),
            identity_card=request.FILES.get('identity_card')
        )

        # Log the user in after successful signup
        login(request, user)
        messages.success(request, "Signup successful. You are now logged in.")
        return redirect('volunteer_login')  # Adjust the redirect URL name if necessary

    return render(request, 'volunteer_signup.html')


def volunteer_login(request):
    error = None
    if request.method == 'POST':
        email = request.POST['email_id']
        pwd = request.POST['password']
        user = authenticate(username=email, password=pwd)
        if user:
            try:
                user1 = Volunteer.objects.get(user=user)
                if user1.status != "pending":
                    login(request, user)
                    error = "no"
                else:
                    error = "not"
            except:
                error = "yes"
        else:
            error = "yes"
    return render(request, 'volunteer_login.html', locals())



def volunteer_base(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')
    return render(request, 'volunteer_base.html')


def Volunteer_home(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')
    return render(request, 'volunteer_home.html')

def active_campaign_volunteer(requests):
    campaigns = Campaign.objects.filter(status='active')
    return render(requests,'active_campaign_volunteer.html', locals())

@login_required
def profile_volunteer(request):
    # Get the current volunteer's profile
    volunteer = get_object_or_404(Volunteer, user=request.user)

    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email_id')
        contact = request.POST.get('phone_number')
        address = request.POST.get('address')
        aboutme = request.POST.get('aboutme')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password and password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('profile_volunteer')

        # Check if password length is sufficient
        if password and len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('profile_volunteer')

        # Update user information
        user = volunteer.user
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        if password:
            user.set_password(password)
        user.save()

        # Update volunteer profile information
        volunteer.contact = contact
        volunteer.address = address
        volunteer.aboutme = aboutme
        if 'profile_pic' in request.FILES:
            volunteer.profile_pic = request.FILES['profile_pic']
        if 'identity_card' in request.FILES:
            volunteer.identity_card = request.FILES['identity_card']
        volunteer.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('profile_volunteer')

    context = {
        'volunteer': volunteer
    }
    return render(request, 'profile_volunteer.html', context)


def volunteer_requests(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    volunteers = Volunteer.objects.filter(status='pending')
    return render(request, 'pending_volunteers.html',  locals())


def accepted_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    volunteers = Volunteer.objects.filter(status='accept')
    return render(request, 'accepted_volunteer.html',  locals())



def rejected_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    volunteers = Volunteer.objects.filter(status='reject')
    return render(request, 'rejected_volunteer.html',  locals())



def all_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    volunteers = Volunteer.objects.all()
    return render(request, 'all_volunteers.html',  locals())


def view_volunteer_details(request, id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    volunteer = Volunteer.objects.get(id=id)

    if request.method == "POST":
        status = request.POST['status']
        adminremark = request.POST['adminremark']

        try:
            volunteer.status = status
            volunteer.admin_remarks = adminremark
            volunteer.updated_at = date.today()
            volunteer.save()

            return render(request, 'view_volunteer_details.html', {'volunteer': volunteer, 'error': 'no'})
        except Exception as e:
            return render(request, 'view_volunteer_details.html', {'volunteer': volunteer, 'error': 'yes'})
    else:
        return render(request, 'view_volunteer_details.html', {'volunteer': volunteer})


@login_required
def edit_volunteer_profile(request):
    volunteer = get_object_or_404(Volunteer, user=request.user)
    
    if request.method == 'POST':
        # Extract data from the POST request
        volunteer.contact = request.POST.get('contact')
        volunteer.address = request.POST.get('address')
        volunteer.aboutme = request.POST.get('aboutme')
        volunteer.status = request.POST.get('status')
        
        # Handle file uploads
        if request.FILES.get('profile_pic'):
            volunteer.profile_pic = request.FILES.get('profile_pic')
        if request.FILES.get('identity_card'):
            volunteer.identity_card = request.FILES.get('identity_card')

        # Save the updated volunteer profile
        volunteer.save()

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('profile_volunteer')  # Redirect to profile page after saving changes

    context = {
        'volunteer': volunteer,
    }

    return render(request, 'edit_volunteer_profile.html', context)

def delete_volunteer(request, id):
    Donor.objects.get(id=id).delete()
    # return redirect('manage_donors')
    
def donation_collection_requests(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    donation = Donation.objects.filter(volunteer=volunteer, status='Volunteer Allocated')
    return render(request, 'collection_req.html', locals())



def collection_req_details(request, id):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')
    
    donation = Donation.objects.get(id=id)
    error = ""

    if request.method == "POST":
        status = request.POST['status']
        volunteerremarks = request.POST['volunteerremarks']
 
        try:
            donation.status = status
            donation.volunteer_remarks = volunteerremarks
            donation.updated_at = date.today()
            donation.save()
            error = "no"

            return render(request, 'collection_req_details.html', locals())
        except Exception as e:
            error = "yes"
            return render(request, 'collection_req_details.html', locals())
    else:
        return render(request, 'collection_req_details.html', locals())


    
def donation_received(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')
    
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    donation = Donation.objects.filter(volunteer=volunteer, status='Donation Received')
    return render(request, 'donation_receive.html', locals())


def donation_not_received(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')
    
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    donation = Donation.objects.filter(volunteer=volunteer, status='Donation Not Received')
    return render(request, 'donation_not_received.html', locals())


def donation_rec_details(request, id):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')
    
    donation = Donation.objects.get(id=id)
    error = ""

    if request.method == "POST":
        status = request.POST['status']
 
        try:
            donation.status = status
            donation.updated_at = date.today()
            donation.save()
            Donation_Gallery.objects.create(donation=donation)
            error = "no"

            return render(request, 'donation_rec_detail.html', locals())
        except Exception as e:
            error = "yes"
            return render(request, 'donation_rec_detail.html', locals())
    else:
        return render(request, 'donation_rec_detail.html', locals())
 

@login_required(login_url='volunteer_login')
def donation_delivered(request):
    user = request.user
    
    try:
        volunteer = Volunteer.objects.get(user=user)
    except Volunteer.DoesNotExist:
        messages.error(request, "Volunteer not found.")
        return redirect('some_error_page')

    # Filter donations that have the status 'Donation Delivered Successfully'
    donations = Donation.objects.filter(volunteer=volunteer, status='Donation Delivered Successfully')

    if not donations.exists():
        messages.info(request, "No delivered donations found.")
    
    return render(request, 'donation_delivered.html', {'donations': donations})


@login_required(login_url='volunteer_login')
def donation_delivered_details(request, id):
    user = request.user
    
    # Ensure the volunteer is associated with the donation
    volunteer = get_object_or_404(Volunteer, user=user)
    donation = get_object_or_404(Donation, id=id, volunteer=volunteer, status='Donation Delivered Successfully')
    
    return render(request, 'donation_delivered_details.html', {'donation': donation})





# For esewa payment gateway 


def initiate_payment(request, id):
    if request.method == 'POST':
        # Get amount and campaign_id from POST request
        amount = request.POST.get('amount')
        campaign_id = request.POST.get('campaign_id')

        # Check if campaign_id is provided
        if not campaign_id:
            return HttpResponseBadRequest("Campaign ID is required.")

        # Get donor details from POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Generate a unique transaction ID
        transaction_id = str(uuid.uuid4())
        merchant_code = 'EPAYTEST'

        # Prepare context for payment template
        context = {
            'amount': amount,
            'merchant_code': merchant_code,
            'product_id': campaign_id,
            'transaction_id': transaction_id,
            'success_url': 'http://127.0.0.1:8000/success/',
            'failure_url': 'http://127.0.0.1:8000/failure/',
            'name': name,
            'email': email,
            'phone': phone
        }

        return render(request, 'payment.html', context)
    else:
        return HttpResponse("Invalid request method.", status=405)
    

def payment_success(request, name, email, campaign_id, phone):
    # Get the Base64 encoded string from the request
    encoded_str = request.GET.get('data')

    if not encoded_str:
        return HttpResponseBadRequest("Missing payment data")

    try:
        # Decode the Base64 string to get the original JSON string
        decoded_bytes = base64.b64decode(encoded_str)
        decoded_str = decoded_bytes.decode('utf-8')
        
        # Parse the decoded JSON string
        decoded_json = json.loads(decoded_str)

        # Extract transaction details from the decoded JSON
        amount = decoded_json.get('total_amount', '0').replace(',', '')  # Clean amount
        transaction_id = decoded_json.get("transaction_uuid")

        # Convert the amount to a Decimal object
        donation_amount = Decimal(amount)

    except (json.JSONDecodeError, base64.binascii.Error, Decimal.InvalidOperation) as e:
        # Handle decoding or conversion errors
        return HttpResponseBadRequest(f"Error decoding or converting payment data: {e}")

    # Retrieve the campaign using the campaign_id
    if not campaign_id:
        return HttpResponseBadRequest("Campaign ID is missing in the response.")

    campaign = get_object_or_404(Campaign, id=campaign_id)

    # Update the amount raised in the campaign
    campaign.amount_raised += donation_amount
    campaign.save()

    # Check if the donor already exists (based on email or phone)
    donor, created = Donor.objects.get_or_create(
        phone_number=phone,
        defaults={
            'address': None,
            'district': None,
            'country': None,
            'amount_donated': donation_amount,
            'campaign': campaign,
        }
    )

    # If donor already exists, update the donation amount
    if not created:
        donor.amount_donated += donation_amount
        donor.save()

    # Save donation details in the Donation model
    Donation.objects.create(
        campaign=campaign,
        donor=donor,
        donation_name=f"{name}",
        amount=donation_amount,
        description="Donation made through eSewa",
        status="success",
        user=request.user if request.user.is_authenticated else None,
    )

    # Prepare context for the success page
    context = {
        'ref_id': transaction_id,
        'amount': donation_amount,
        'campaign': campaign,
        'donor': donor,
    }

    return render(request, 'esewa_success.html', context)

def payment_failure(request):
    return render(request, 'esewa_failure.html')





### For campaign management 
@login_required
def create_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.created_by = request.user
            campaign.save()
            return redirect('campaign_list')
    else:
        form = CampaignForm()
    return render(request, 'campaign/create_campaign.html', {'form': form})

@login_required
def update_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            return redirect('campaign_list')
    else:
        form = CampaignForm(instance=campaign)
    return render(request, 'campaign/update_campaign.html', {'form': form, 'campaign': campaign})

@login_required
def delete_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if request.method == 'POST':
        campaign.delete()
        return redirect('campaign_list')
    return render(request, 'campaign/delete_campaign.html', {'campaign': campaign})

@login_required
def campaign_list(request):
    campaigns = Campaign.objects.all().order_by('-created_at')
    return render(request, 'campaign/campaign_list.html', {'campaigns': campaigns})


@login_required
def active_campaign(request):
    campaigns = Campaign.objects.filter(status='active')
    return render(request, 'campaign/active_campaign.html', {'campaigns': campaigns})

@login_required
def campaign_detail(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    return render(request, 'campaign/campaign_detail.html', {'campaign': campaign})


def campaign_learn_more(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    return render(request, 'campaign/learn_more.html', {'campaign': campaign})


def campaign_donations(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    donations = Donation.objects.filter(user__isnull=False) 
    return render(request, 'campaign/campaign_donations.html', {'donations': donations})



def campaign_donation_details(request, pid):
    donation = get_object_or_404(Donation, id=pid)
    
    context = {
        'donation': donation,
    }
    return render(request, 'campaign/campaign_donation_details.html', context)


def DonateView(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    return render(request, 'payment.html', {'campaign': campaign})

    # def post(self, request, campaign_id, amount):
    #     # Process the donation
    #     campaign = get_object_or_404(Campaign, id=campaign_id)
        
    #     # Simulate successful payment
    #     payment_success = True
        
    #     if payment_success:
    #         campaign.amount_raised += amount
    #         campaign.save()

    #         messages.success(request, f'Thank you for your donation of ${amount} to {campaign.title}!')
    #         return redirect('campaign_detail', campaign_id=campaign.id)
    #     else:
    #         messages.error(request, 'There was an error processing your donation. Please try again.')
    #         return redirect('donate', campaign_id=campaign.id)
        
# Logout for all users.
def Logout(request):
    logout(request)
    return redirect('homepage')


