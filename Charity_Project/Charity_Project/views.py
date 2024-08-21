from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.middleware.csrf import get_token
from donor_management.models import Donor, Donation, DonationArea, Volunteer, ContactMessage
from django.contrib.auth import login, logout, authenticate
from datetime import date

def homepage(request):
 return render(request, 'homepage.html')

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

# For login and signup 

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def login_as_view(request):
    return render(request, 'login_as.html')

def signup_as_view(request):
   return render(request, 'signup_as.html')



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
def admin_signup(request):
    return render(request, 'admin_signup.html')


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
    # total_campaigns = Campaign.objects.count()
    total_donations = Donation.objects.count()
    active_volunteers = Volunteer.objects.filter(status='active').count()

    context = {
        'total_donors': total_donors,
        # 'total_campaigns': total_campaigns,
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
        return redirect('admin_login')
    donations = Donation.objects.filter(status='accept')
    return render(request, 'accepted_donations.html',  locals())

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

def delete_area(request, area_id):
    DonationArea.objects.get(id=area_id).delete()
    return redirect('manage_area')
    

def manage_donors(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donors = Donor.objects.all()
    return render(request, 'manage_donors.html',  locals())

def view_donors_details(request, id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    donors = Donor.objects.get(id=id)
    return render(request, 'view_donors_details.html', locals())


def delete_donors(request, donor_id):
    Donor.objects.get(id=donor_id).delete()
    return redirect('manage_donors')
    
def inquires_view(request):
    messages = ContactMessage.objects.all()
    return render(request, 'inquires.html', {'messages': messages})

def view_message_details(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    return render(request, 'inquires_details.html', {'message': message})

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
            status='pending'
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








# Logout for all users.
def Logout(request):
    logout(request)
    return redirect('homepage')


