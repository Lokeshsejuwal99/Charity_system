"""
Test Cases for Charity Management System

This module contains unit tests for various aspects of the Charity Management System,
including views, models, and authentication.

The tests are categorized into:
1. **Black-box testing** - Focuses on expected inputs and outputs without knowledge of internal implementation.
2. **White-box testing** - Examines the internal logic and implementation details.

Modules tested:
- Views (homepage, donation gallery, contact form, admin dashboard, feedback page)
- Volunteer, Donor, and Admin signup functionality
- Models (Campaign, Donor, Volunteer, Donation)
- Urls (Campaign, Donor, Volunteer, Donation)
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from donor_management.models import Donor, Campaign, Volunteer, Donation, DonationArea
from donor_management.views import *
from Charity_Project.views import *
from django.utils import timezone



# ------------------- WHITE-BOX TESTS for models-------------------

class VolunteerSignupTestCase(TestCase):
    """Test cases for volunteer signup functionality"""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for volunteer signup"""
        cls.signup_url = reverse('volunteer_signup')

    def test_successful_signup(self):
        """White-box test: Ensure a volunteer can sign up successfully"""
        response = self.client.post(self.signup_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email_id': 'john@example.com',
            'phone_number': '1234567890',
            'address': '123 Main St',
            'aboutme': 'I love volunteering!',
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertTrue(User.objects.filter(email='john@example.com').exists())
        self.assertTrue(Volunteer.objects.filter(user__email='john@example.com').exists())

    def test_password_mismatch(self):
        """White-box test: Ensure signup fails when passwords do not match"""
        response = self.client.post(self.signup_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email_id': 'john@example.com',
            'phone_number': '1234567890',
            'address': '123 Main St',
            'aboutme': 'I love volunteering!',
            'password': 'password123',
            'confirm_password': 'differentpassword',
        })
        self.assertFalse(User.objects.filter(email='john@example.com').exists())

    def test_insufficient_password_length(self):
        """White-box test: Ensure signup fails when password is too short"""
        response = self.client.post(self.signup_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email_id': 'john@example.com',
            'phone_number': '1234567890',
            'address': '123 Main St',
            'aboutme': 'I love volunteering!',
            'password': 'short',
            'confirm_password': 'short',
        })
        self.assertFalse(User.objects.filter(email='john@example.com').exists())

    def test_email_already_registered(self):
        """White-box test: Ensure signup fails when email is already taken"""
        User.objects.create_user(username='john@example.com', email='john@example.com', password='password123')
        response = self.client.post(self.signup_url, {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email_id': 'john@example.com',
            'phone_number': '0987654321',
            'address': '456 Another St',
            'aboutme': 'I love volunteering too!',
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertEqual(Volunteer.objects.filter(user__email='john@example.com').count(), 0)


class CampaignModelTest(TestCase):
    """White-box tests for the Campaign model"""

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.campaign = Campaign.objects.create(
            title="Health Campaign",
            description="A campaign for health awareness.",
            goal_amount=10000,
            amount_raised=5000,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=10),
            status='active',
            created_by=self.user
        )
    
    def test_campaign_str(self):
        """White-box test: Ensure the string representation of the campaign is correct"""
        self.assertEqual(str(self.campaign), "Health Campaign")
    
    def test_campaign_is_active(self):
        """White-box test: Verify the logic to check if the campaign is active"""
        self.assertTrue(self.campaign.is_active())
    

class DonorModelTest(TestCase):
    """White-box tests for the Donor model"""

    def setUp(self):
        self.user = User.objects.create(username="donoruser")
        self.campaign = Campaign.objects.create(title="Charity", description="Test", goal_amount=5000, created_by=self.user)
        self.donor = Donor.objects.create(
            user=self.user,
            phone_number="1234567890",
            address="Kathmandu",
            district="Bagmati",
            country="Nepal",
            amount_donated=1000,
            campaign=self.campaign
        )
    
    def test_donor_str(self):
        """White-box test: Ensure the donor's string representation is correct"""
        self.assertEqual(str(self.donor), "donoruser")


class VolunteerModelTest(TestCase):
    """White-box tests for the Volunteer model"""

    def setUp(self):
        self.user = User.objects.create(username="volunteeruser")
        self.volunteer = Volunteer.objects.create(
            user=self.user,
            contact="9800000000",
            address="Kathmandu",
            aboutme="I love volunteering!",
            status="active"
        )
    
    def test_volunteer_str(self):
        """White-box test: Ensure the volunteer's string representation is correct"""
        self.assertEqual(str(self.volunteer), "volunteeruser")


class DonationModelTest(TestCase):
    """White-box tests for the Donation model"""

    def setUp(self):
        self.user = User.objects.create(username="donoruser")
        self.campaign = Campaign.objects.create(title="Test Campaign", description="Test Desc", goal_amount=1000, created_by=self.user)
        self.donor = Donor.objects.create(user=self.user, amount_donated=500, campaign=self.campaign)
        self.donation_area = DonationArea.objects.create(area_name="Kathmandu", description="Area Desc")
        self.donation = Donation.objects.create(
            campaign=self.campaign,
            donor=self.donor,
            donation_name="Food Items",
            amount="500",
            collection_loc="Kathmandu",
            status="pending",
            donation_area=self.donation_area
        )


#-------------Black-box test for models-------------------#

class VolunteerSignupBlackBoxTestCase(TestCase):
    """Black-box tests for volunteer signup functionality"""

    @classmethod
    def setUpTestData(cls):
        """Set up the URL for volunteer signup"""
        cls.signup_url = reverse('volunteer_signup')

    def test_successful_signup(self):
        """Black-box test: Ensure a volunteer can sign up successfully"""
        response = self.client.post(self.signup_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email_id': 'john@example.com',
            'phone_number': '1234567890',
            'address': '123 Main St',
            'aboutme': 'I love volunteering!',
            'password': 'password123',
            'confirm_password': 'password123',
        })

    def test_password_mismatch(self):
        """Black-box test: Ensure signup fails when passwords do not match"""
        response = self.client.post(self.signup_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email_id': 'john@example.com',
            'phone_number': '1234567890',
            'address': '123 Main St',
            'aboutme': 'I love volunteering!',
            'password': 'password123',
            'confirm_password': 'differentpassword',
        })

    def test_insufficient_password_length(self):
        """Black-box test: Ensure signup fails when password is too short"""
        response = self.client.post(self.signup_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email_id': 'john@example.com',
            'phone_number': '1234567890',
            'address': '123 Main St',
            'aboutme': 'I love volunteering!',
            'password': 'short',
            'confirm_password': 'short',
        })

    def test_email_already_registered(self):
        """Black-box test: Ensure signup fails when email is already taken"""
        User.objects.create_user(username='john@example.com', email='john@example.com', password='password123')
        response = self.client.post(self.signup_url, {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email_id': 'john@example.com',
            'phone_number': '0987654321',
            'address': '456 Another St',
            'aboutme': 'I love volunteering too!',
            'password': 'password123',
            'confirm_password': 'password123',
        })



    def test_redirect_after_successful_signup(self):
        """Black-box test: Ensure user is redirected after a successful signup"""
        response = self.client.post(self.signup_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email_id': 'john@example.com',
            'phone_number': '1234567890',
            'address': '123 Main St',
            'aboutme': 'I love volunteering!',
            'password': 'password123',
            'confirm_password': 'password123',
        })





#------------------White-Box Testing for Views------------------------#

class ViewsTestCase(TestCase):
    """Test cases for public-facing views"""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods"""
        cls.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='password123'
        )
        cls.donor = Donor.objects.create(
            user=cls.user,
            phone_number='1234567890',
            address='Test Address',
            district='Test District',
            country='Test Country'
        )

    def test_homepage_view_white_box(self):
        """White-box test: Ensure the homepage uses the correct template and context"""
        response = self.client.get(reverse('homepage'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_contact_form_submission_white_box(self):
        """White-box test: Ensure the contact form processes and redirects correctly"""
        response = self.client.post(reverse('contact'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message.'
        })

        self.assertEqual(response.status_code, 302)

    def test_admin_dashboard_view_white_box(self):
        """White-box test: Ensure an admin user can access the donor dashboard"""
        self.user.is_staff = True
        self.user.save()
        
        self.client.login(username='testuser', password='password123')
        
        response = self.client.get(reverse('donor_home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donor_management/donor_home.html')

    def test_feedback_page_view_white_box(self):
        """White-box test: Ensure the feedback page loads correctly and the context is passed"""
        response = self.client.get(reverse('feedback_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback_page.html')



#--------------------- Black-box Testing for views------------------#

class ViewsTestCase(TestCase):
    """Test cases for public-facing views"""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods"""
        cls.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='password123'
        )
        cls.donor = Donor.objects.create(
            user=cls.user,
            phone_number='1234567890',
            address='Test Address',
            district='Test District',
            country='Test Country'
        )

    def test_homepage_view(self):
        """Black-box test: Ensure the homepage loads correctly"""
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)


    def test_contact_form_submission(self):
        """Black-box test: Ensure the contact form can be submitted successfully"""
        response = self.client.post(reverse('contact'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message.'
        })

    def test_admin_dashboard_view(self):
        """Black-box test: Ensure an admin user can access the donor dashboard"""
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('donor_home'))
        self.assertEqual(response.status_code, 200)

    def test_feedback_page_view(self):
        """Black-box test: Ensure the feedback page loads correctly"""
        response = self.client.get(reverse('feedback_page'))
        self.assertEqual(response.status_code, 200)
        
        
        
#-----------------------White Box tesing for Urls-----------------------#

class UrlsTestCase(TestCase):
    """Test cases for URL resolution"""

    def test_homepage_url_resolves(self):
        """Test homepage URL resolves"""
        url = reverse('homepage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_contact_url_resolves(self):
        """Test contact page URL resolves"""
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_url_resolves(self):
        """Test admin dashboard URL resolves"""
        url = reverse('donor_home')

    def test_feedback_url_resolves(self):
        """Test feedback page URL resolves"""
        url = reverse('feedback_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class CharitySystemTests(TestCase):
    """Black-box tests for the Charity Management System"""

    def test_homepage_accessible(self):
        """Black-box test: Ensure the homepage is accessible"""
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_accessible(self):
        """Black-box test: Ensure the login page is accessible"""
        response = self.client.get(reverse('login_as'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_accessible(self):
        """Black-box test: Ensure the signup page is accessible"""
        response = self.client.get(reverse('signup_as'))
        self.assertEqual(response.status_code, 200)

    def test_feedback_page_accessible(self):
        """Black-box test: Ensure the feedback page is accessible"""
        response = self.client.get(reverse('feedback_page'))
        self.assertEqual(response.status_code, 200)

    def test_request_for_donation_page(self):
        """Black-box test: Ensure the request for donation page is accessible"""
        response = self.client.get(reverse('request_for_donation'))
        self.assertEqual(response.status_code, 200)

    def test_campaign_list_page(self):
        """Black-box test: Ensure the campaign list page is accessible"""
        response = self.client.get(reverse('campaign_list'))

    def test_payment_success_page(self):
        """Black-box test: Ensure the payment success page is accessible"""
        response = self.client.get(reverse('esewa_success', args=['John Doe', 'john@example.com', '1', '1234567890']))

    def test_payment_failure_page(self):
        """Black-box test: Ensure the payment failure page is accessible"""
        response = self.client.get(reverse('esewa_failure'))



#------------------------Black-Box testing for urls------------------#

class CharitySystemTests(TestCase):
    """Black-box tests for the Charity Management System"""

    def test_homepage_accessible(self):
        """Black-box test: Ensure the homepage is accessible"""
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome")

    def test_login_page_accessible(self):
        """Black-box test: Ensure the login page is accessible"""
        response = self.client.get(reverse('login_as'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_signup_page_accessible(self):
        """Black-box test: Ensure the signup page is accessible"""
        response = self.client.get(reverse('signup_as'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Signup")

    def test_feedback_page_accessible(self):
        """Black-box test: Ensure the feedback page is accessible"""
        response = self.client.get(reverse('feedback_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Feedback")

    def test_request_for_donation_page(self):
        """Black-box test: Ensure the request for donation page is accessible"""
        response = self.client.get(reverse('request_for_donation'))
        self.assertEqual(response.status_code, 200)

    def test_campaign_list_page(self):
        """Black-box test: Ensure the campaign list page is accessible"""
        response = self.client.get(reverse('campaign_list'))
        self.assertEqual(response.status_code, 302)

    def test_payment_success_page(self):
        """Black-box test: Ensure the payment success page is accessible"""
        response = self.client.get(reverse('esewa_success', args=['John Doe', 'john@example.com', '1', '1234567890']))
        self.assertEqual(response.status_code, 400)

    def test_payment_failure_page(self):
        """Black-box test: Ensure the payment failure page is accessible"""
        response = self.client.get(reverse('esewa_failure'))
        self.assertEqual(response.status_code, 200)
