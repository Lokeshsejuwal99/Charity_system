# # charity_app/tests/test_models.py

# from django.test import TestCase
# from django.contrib.auth.models import User
# from django.utils import timezone
# from decimal import Decimal
# from .models import (
#     Campaign, Donor, Volunteer, DonationArea, Donation,
#     Request_for_donation, Donation_Gallery, ContactMessage, Feedback
# )

# class CampaignModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='campaign_creator', password='testpass')
#         self.campaign = Campaign.objects.create(
#             title='Test Campaign',
#             description='This is a test campaign.',
#             goal_amount=Decimal('1000.00'),
#             amount_raised=Decimal('250.00'),
#             start_date=timezone.now(),
#             end_date=timezone.now() + timezone.timedelta(days=10),
#             status='active',
#             created_by=self.user
#         )

#     def test_campaign_creation(self):
#         """Test that a campaign is created with correct attributes."""
#         self.assertEqual(self.campaign.title, 'Test Campaign')
#         self.assertEqual(str(self.campaign), 'Test Campaign')

#     def test_is_active(self):
#         """Test the is_active method for a campaign."""
#         self.assertTrue(self.campaign.is_active())

#     def test_progress_percentage(self):
#         """Test the progress_percentage property."""
#         expected_percentage = (self.campaign.amount_raised / self.campaign.goal_amount) * 100
#         self.assertEqual(self.campaign.progress_percentage, expected_percentage)

# class DonorModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='donoruser', password='donorpass')
#         self.campaign = Campaign.objects.create(
#             title='Donor Campaign',
#             description='Campaign for donor test.',
#             goal_amount=Decimal('500.00'),
#             start_date=timezone.now(),
#             end_date=timezone.now() + timezone.timedelta(days=5),
#             status='active',
#             created_by=self.user
#         )
#         self.donor = Donor.objects.create(
#             user=self.user,
#             phone_number='1234567890',
#             address='123 Main St',
#             district='District A',
#             country='Country X',
#             amount_donated=Decimal('100.00'),
#             campaign=self.campaign
#         )

#     def test_donor_creation(self):
#         """Test that a donor is created and linked to a user."""
#         self.assertEqual(self.donor.user.username, 'donoruser')
#         self.assertEqual(str(self.donor), 'donoruser')

#     def test_donor_amount(self):
#         """Test that the donor's amount donated is correct."""
#         self.assertEqual(self.donor.amount_donated, Decimal('100.00'))

# class VolunteerModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='volunteeruser', password='volunteerpass')
#         self.volunteer = Volunteer.objects.create(
#             user=self.user,
#             contact='0987654321',
#             address='456 Elm St',
#             aboutme='I love volunteering.',
#             status='active',
#             admin_remarks='Good volunteer.'
#         )

#     def test_volunteer_creation(self):
#         """Test that a volunteer is created and linked to a user."""
#         self.assertEqual(self.volunteer.user.username, 'volunteeruser')
#         self.assertEqual(str(self.volunteer), 'volunteeruser')

#     def test_volunteer_status(self):
#         """Test that the volunteer's status is set correctly."""
#         self.assertEqual(self.volunteer.status, 'active')

# class DonationAreaModelTest(TestCase):
#     def setUp(self):
#         self.donation_area = DonationArea.objects.create(
#             area_name='Area 1',
#             description='Area for donations.'
#         )

#     def test_donation_area_creation(self):
#         """Test that a donation area is created with correct attributes."""
#         self.assertEqual(self.donation_area.area_name, 'Area 1')
#         self.assertEqual(str(self.donation_area), 'Area 1')

# class DonationModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='donoruser', password='donorpass')
#         self.campaign = Campaign.objects.create(
#             title='Donation Campaign',
#             description='Campaign for donation test.',
#             goal_amount=Decimal('2000.00'),
#             start_date=timezone.now(),
#             end_date=timezone.now() + timezone.timedelta(days=20),
#             status='active',
#             created_by=self.user
#         )
#         self.donor = Donor.objects.create(
#             user=self.user,
#             phone_number='1234567890',
#             address='123 Main St',
#             district='District A',
#             country='Country X',
#             amount_donated=Decimal('200.00'),
#             campaign=self.campaign
#         )
#         self.volunteer_user = User.objects.create_user(username='volunteeruser', password='volunteerpass')
#         self.volunteer = Volunteer.objects.create(
#             user=self.volunteer_user,
#             contact='0987654321',
#             address='456 Elm St',
#             aboutme='Volunteer for donations.',
#             status='active'
#         )
#         self.donation_area = DonationArea.objects.create(
#             area_name='Area 2',
#             description='Another area for donations.'
#         )
#         self.donation = Donation.objects.create(
#             campaign=self.campaign,
#             donor=self.donor,
#             donation_name='Test Donation',
#             amount='150.00',
#             collection_loc='Location A',
#             description='Testing donation.',
#             status='pending',
#             volunteer=self.volunteer,
#             donation_area=self.donation_area,
#             user=self.user
#         )

#     def test_donation_creation(self):
#         """Test that a donation is created with correct attributes."""
#         self.assertEqual(self.donation.donation_name, 'Test Donation')
#         self.assertEqual(str(self.donation), f"{self.donor.user} {self.donor.user}")

#     def test_donation_status(self):
#         """Test that the donation status is set correctly."""
#         self.assertEqual(self.donation.status, 'pending')

# class RequestForDonationModelTest(TestCase):
#     def setUp(self):
#         self.request = Request_for_donation.objects.create(
#             name='John Doe',
#             contact_no=1234567890,
#             request_for='Need help with food supplies.'
#         )

#     def test_request_creation(self):
#         """Test that a request for donation is created correctly."""
#         self.assertEqual(self.request.name, 'John Doe')
#         self.assertEqual(str(self.request), 'John Doe')

# class DonationGalleryModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='donoruser', password='donorpass')
#         self.donor = Donor.objects.create(user=self.user)
#         self.donation = Donation.objects.create(
#             donor=self.donor,
#             donation_name='Gallery Donation',
#             amount='100.00'
#         )
#         self.gallery = Donation_Gallery.objects.create(
#             donation=self.donation,
#             # Assuming you handle null values for delivery_pic
#             delivery_pic=None
#         )

#     def test_gallery_creation(self):
#         """Test that a donation gallery is created correctly."""
#         self.assertEqual(self.gallery.donation.donation_name, 'Gallery Donation')
#         self.assertEqual(str(self.gallery), 'Gallery Donation')

# class ContactMessageModelTest(TestCase):
#     def setUp(self):
#         self.message = ContactMessage.objects.create(
#             name='Jane Smith',
#             email='jane@example.com',
#             message='I am interested in volunteering.'
#         )

#     def test_contact_message_creation(self):
#         """Test that a contact message is created correctly."""
#         self.assertEqual(self.message.name, 'Jane Smith')
#         self.assertEqual(str(self.message), 'Message from Jane Smith (jane@example.com)')

# class FeedbackModelTest(TestCase):
#     def setUp(self):
#         self.feedback = Feedback.objects.create(
#             name='Alice Johnson',
#             email='alice@example.com',
#             message='Great work on the campaign!'
#         )

#     def test_feedback_creation(self):
#         """Test that feedback is created correctly."""
#         self.assertEqual(self.feedback.name, 'Alice Johnson')
#         self.assertEqual(str(self.feedback), 'Alice Johnson')


# from django.test import SimpleTestCase
# from django.urls import reverse, resolve
# from Charity_Project.views import (
#     homepage, login_as_view, donation_gallery, signup_as_view, about_view, contact_view,
#     feedback_page, request_for_donation, thank_you, campaign_list, create_campaign, 
#     active_campaign, DonateView, campaign_detail, campaign_learn_more, update_campaign, 
#     delete_campaign, campaign_donation_details, admin_login, admin_dashboard, 
#     inquires_view, view_message_details, feedback_list_admin, view_feedback, delete_feedback, 
#     pending_donations, accepted_donations, view_donation, accepted_donation_details, guest_donations, 
#     add_donation_area, manage_donation_area, edit_donation_area, delete_area, manage_donors, 
#     view_donors_details, delete_donors, donation_requests_view, donation_requests_details_view, 
#     volunteer_signup, volunteer_login, volunteer_base, Volunteer_home, profile_volunteer, 
#     active_campaign_volunteer, volunteer_requests, accepted_volunteer, rejected_volunteer, 
#     all_volunteer, view_volunteer_details, edit_volunteer_profile, delete_volunteer, donation_collection_requests, 
#     collection_req_details, donation_received, donation_not_received, donation_rec_details, 
#     donation_delivered, donation_delivered_details, donor_login, donor_signup, Logout, 
#     initiate_payment, payment_success, payment_failure, campaign_donations
# )


# class TestURLs(SimpleTestCase):

#     def test_homepage_url(self):
#         url = reverse('homepage')
#         self.assertEqual(resolve(url).func, homepage)

#     def test_login_as_url(self):
#         url = reverse('login_as')
#         self.assertEqual(resolve(url).func, login_as_view)

#     def test_donation_gallery_url(self):
#         url = reverse('donation_gallery')
#         self.assertEqual(resolve(url).func, donation_gallery)

#     def test_signup_as_url(self):
#         url = reverse('signup_as')
#         self.assertEqual(resolve(url).func, signup_as_view)

#     def test_about_url(self):
#         url = reverse('about')
#         self.assertEqual(resolve(url).func, about_view)

#     def test_contact_url(self):
#         url = reverse('contact')
#         self.assertEqual(resolve(url).func, contact_view)

#     def test_feedback_page_url(self):
#         url = reverse('feedback_page')
#         self.assertEqual(resolve(url).func, feedback_page)

#     def test_request_for_donation_url(self):
#         url = reverse('request_for_donation')
#         self.assertEqual(resolve(url).func, request_for_donation)

#     def test_thank_you_url(self):
#         url = reverse('thank_you')
#         self.assertEqual(resolve(url).func, thank_you)

#     def test_campaign_list_url(self):
#         url = reverse('campaign_list')
#         self.assertEqual(resolve(url).func, campaign_list)

#     def test_create_campaign_url(self):
#         url = reverse('create_campaign')
#         self.assertEqual(resolve(url).func, create_campaign)

#     def test_active_campaign_url(self):
#         url = reverse('active_campaign')
#         self.assertEqual(resolve(url).func, active_campaign)

#     def test_donate_campaign_url(self):
#         url = reverse('donate', args=[1])
#         self.assertEqual(resolve(url).func, DonateView)

#     def test_campaign_detail_url(self):
#         url = reverse('campaign_detail', args=[1])
#         self.assertEqual(resolve(url).func, campaign_detail)

#     def test_campaign_learn_more_url(self):
#         url = reverse('campaign_learn_more', args=[1])
#         self.assertEqual(resolve(url).func, campaign_learn_more)

#     def test_update_campaign_url(self):
#         url = reverse('update_campaign', args=[1])
#         self.assertEqual(resolve(url).func, update_campaign)

#     def test_delete_campaign_url(self):
#         url = reverse('delete_campaign', args=[1])
#         self.assertEqual(resolve(url).func, delete_campaign)

#     def test_campaign_donation_details_url(self):
#         url = reverse('campaign_donation_details', args=[1])
#         self.assertEqual(resolve(url).func, campaign_donation_details)

#     def test_admin_login_url(self):
#         url = reverse('admin_login')
#         self.assertEqual(resolve(url).func, admin_login)

#     def test_admin_home_url(self):
#         url = reverse('admin_home')
#         self.assertEqual(resolve(url).func, admin_dashboard)

#     def test_inquires_url(self):
#         url = reverse('inquires')
#         self.assertEqual(resolve(url).func, inquires_view)

#     def test_view_message_details_url(self):
#         url = reverse('view_message_details', args=[1])
#         self.assertEqual(resolve(url).func, view_message_details)

#     def test_feedback_list_admin_url(self):
#         url = reverse('feedback_list_admin')
#         self.assertEqual(resolve(url).func, feedback_list_admin)

#     def test_view_feedback_url(self):
#         url = reverse('view_feedback', args=[1])
#         self.assertEqual(resolve(url).func, view_feedback)

#     def test_delete_feedback_url(self):
#         url = reverse('delete_feedback', args=[1])
#         self.assertEqual(resolve(url).func, delete_feedback)

#     def test_pending_donations_url(self):
#         url = reverse('pending_donations')
#         self.assertEqual(resolve(url).func, pending_donations)

#     def test_accepted_donations_url(self):
#         url = reverse('accepted_donations')
#         self.assertEqual(resolve(url).func, accepted_donations)

#     def test_view_donation_url(self):
#         url = reverse('view_donation', args=[1])
#         self.assertEqual(resolve(url).func, view_donation)

#     def test_accepted_donation_details_url(self):
#         url = reverse('accepted_donation_details', args=[1])
#         self.assertEqual(resolve(url).func, accepted_donation_details)

#     def test_guest_donations_url(self):
#         url = reverse('guest_donations')
#         self.assertEqual(resolve(url).func, guest_donations)

#     def test_add_area_url(self):
#         url = reverse('add_area')
#         self.assertEqual(resolve(url).func, add_donation_area)

#     def test_manage_area_url(self):
#         url = reverse('manage_area')
#         self.assertEqual(resolve(url).func, manage_donation_area)

#     def test_edit_donation_area_url(self):
#         url = reverse('edit_donation_area', args=[1])
#         self.assertEqual(resolve(url).func, edit_donation_area)

#     def test_delete_area_url(self):
#         url = reverse('delete_area', args=[1])
#         self.assertEqual(resolve(url).func, delete_area)

#     def test_manage_donors_url(self):
#         url = reverse('manage_donors')
#         self.assertEqual(resolve(url).func, manage_donors)

#     def test_view_donor_details_url(self):
#         url = reverse('view_donors_details', args=[1])
#         self.assertEqual(resolve(url).func, view_donors_details)

#     def test_delete_donors_url(self):
#         url = reverse('delete_donors', args=[1])
#         self.assertEqual(resolve(url).func, delete_donors)

#     def test_donation_requests_view_url(self):
#         url = reverse('donation_requests_view')
#         self.assertEqual(resolve(url).func, donation_requests_view)

#     def test_donation_request_detail_url(self):
#         url = reverse('donation_request_detail', args=[1])
#         self.assertEqual(resolve(url).func, donation_requests_details_view)

#     def test_volunteer_signup_url(self):
#         url = reverse('volunteer_signup')
#         self.assertEqual(resolve(url).func, volunteer_signup)

#     def test_volunteer_login_url(self):
#         url = reverse('volunteer_login')
#         self.assertEqual(resolve(url).func, volunteer_login)

#     def test_volunteer_base_url(self):
#         url = reverse('volunteer_base')
#         self.assertEqual(resolve(url).func, volunteer_base)

#     def test_volunteer_home_url(self):
#         url = reverse('Volunteer_home')
#         self.assertEqual(resolve(url).func, Volunteer_home)

#     def test_profile_volunteer_url(self):
#         url = reverse('profile_volunteer')
#         self.assertEqual(resolve(url).func, profile_volunteer)

#     def test_active_campaign_volunteer_url(self):
#         url = reverse('active_campaign_volunteer')
#         self.assertEqual(resolve(url).func, active_campaign_volunteer)

#     def test_volunteer_requests_url(self):
#         url = reverse('volunteer_requests')
#         self.assertEqual(resolve(url).func, volunteer_requests)

#     def test_accepted_volunteer_url(self):
#         url = reverse('accepted_volunteer')
#         self.assertEqual(resolve(url).func, accepted_volunteer)

#     def test_rejected_volunteer_url(self):
#         url = reverse('rejected_volunteer')
#         self.assertEqual(resolve(url).func, rejected_volunteer)

#     def test_all_volunteer_url(self):
#         url = reverse('all_volunteer')
#         self.assertEqual(resolve(url).func, all_volunteer)

#     def test_view_volunteer_details_url(self):
#         url = reverse('view_volunteer_details', args=[1])
#         self.assertEqual(resolve(url).func, view_volunteer_details)

#     def test_edit_volunteer_url(self):
#         url = reverse('edit_volunteer_profile')
#         self.assertEqual(resolve(url).func, edit_volunteer_profile)

#     def test_delete_volunteer_url(self):
#         url = reverse('delete_volunteer', args=[1])
#         self.assertEqual(resolve(url).func, delete_volunteer)


#     def test_collection_request_details_url(self):
#         url = reverse('collection_req_details', args=[1])
#         self.assertEqual(resolve(url).func, collection_req_details)

#     def test_donation_received_details_url(self):
#         url = reverse('donation_rec_details', args=[1])
#         self.assertEqual(resolve(url).func, donation_rec_details)

#     def test_donation_delivered_details_url(self):
#         url = reverse('donation_delivered_details', args=[1])
#         self.assertEqual(resolve(url).func, donation_delivered_details)

#     def test_donor_login_url(self):
#         url = reverse('donor_login')
#         self.assertEqual(resolve(url).func, donor_login)

#     def test_donor_signup_url(self):
#         url = reverse('donor_signup')
#         self.assertEqual(resolve(url).func, donor_signup)

#     def test_logout_url(self):
#         url = reverse('logout')
#         self.assertEqual(resolve(url).func, Logout)

#     def test_initiate_payment_url(self):
#         url = reverse('initiate_payment', args=[1])
#         self.assertEqual(resolve(url).func, initiate_payment)


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from donor_management.models import Donor, Campaign, Donation, ContactMessage, Volunteer  


class ViewsTestCase(TestCase):
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='password123'
        )
        self.donor = Donor.objects.create(
            user=self.user,
            phone_number='1234567890',
            address='Test Address',
            district='Test District',
            country='Test Country'
        )

    def test_homepage_view(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_donation_gallery_view(self):
        response = self.client.get(reverse('donation_gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery.html')

    def test_contact_view_post(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message.'
        })
        self.assertRedirects(response, reverse('contact'))
        self.assertEqual(ContactMessage.objects.count(), 1)


    def test_admin_dashboard_view(self):
        # Log in the user as an admin
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='testuser', password='password123')
        
        response = self.client.get(reverse('donor_home'))
        self.assertEqual(response.status_code, 200)
 

    def test_feedback_page_view(self):
        response = self.client.get(reverse('feedback_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback_page.html')


class VolunteerSignupTestCase(TestCase):
    def setUp(self):
        self.url = reverse('volunteer_signup')  # Update with the actual name of your URL pattern

    def test_successful_signup(self):
        response = self.client.post(self.url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email_id': 'john@example.com',
            'phone_number': '1234567890',
            'address': '123 Main St',
            'aboutme': 'I love volunteering!',
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertTrue(User.objects.filter(email='john@example.com').exists())
        self.assertTrue(Volunteer.objects.filter(user__email='john@example.com').exists())

    def test_password_mismatch(self):
        response = self.client.post(self.url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email_id': 'john@example.com',
            'phone_number': '1234567890',
            'address': '123 Main St',
            'aboutme': 'I love volunteering!',
            'password': 'password123',
            'confirm_password': 'differentpassword',
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect due to error
        self.assertEqual(len(response.wsgi_request._messages), 1)  # Check for error message

    def test_insufficient_password_length(self):
        response = self.client.post(self.url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email_id': 'john@example.com',
            'phone_number': '1234567890',
            'address': '123 Main St',
            'aboutme': 'I love volunteering!',
            'password': 'short',
            'confirm_password': 'short',
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect due to error
        self.assertEqual(len(response.wsgi_request._messages), 1)  # Check for error message

    def test_email_already_registered(self):
        User.objects.create_user(username='john@example.com', email='john@example.com', password='password123')
        response = self.client.post(self.url, {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email_id': 'john@example.com',
            'phone_number': '0987654321',
            'address': '456 Another St',
            'aboutme': 'I love volunteering too!',
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect due to error
        self.assertEqual(len(response.wsgi_request._messages), 1)  # Check for error message