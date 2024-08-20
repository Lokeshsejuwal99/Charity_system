from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.middleware.csrf import get_token
from donor_management.models import Donor, Donation, DonationArea, Volunteer
from django.contrib.auth import login, logout, authenticate
from datetime import date

def homepage(request):
 return render(request, 'homepage.html')

def about_view(request):
 return render(request, 'about.html')

def contact_view(request):
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


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'admin_home.html')


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


def volunteer_requests(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    volunteers = Volunteer.objects.filter(status='pending')
    return render(request, 'volunteer_requests.html',  locals())


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
    









# Logout for all users.
def Logout(request):
    logout(request)
    return redirect('homepage')


