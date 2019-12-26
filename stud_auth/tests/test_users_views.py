from django.test import TestCase, override_settings, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


@override_settings(LANGUAGE_CODE='en')
class TestUsersList(TestCase):

    fixtures = ['stud_auth_test_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('users_list')

    def test_access(self):
        response = self.client.get(self.url, follow=True)
        # status code 200
        self.assertEqual(response.status_code, 200)
        # login page
        self.assertIn('Log in', response.content)
        # right link
        self.assertEqual(response.redirect_chain[0][0],
                     'http://testserver/users/login/?next=/users/profiles/')


@override_settings(LANGUAGE_CODE='en')
class TestProfile(TestCase):

    fixtures = ['stud_auth_test_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('profile')

    def test_access(self):
        response = self.client.get(self.url, follow=True)
        # status code 200
        self.assertEqual(response.status_code, 200)
        # login page
        self.assertIn('Log in', response.content)
        # right link
        self.assertEqual(response.redirect_chain[0][0],
             'http://testserver/users/login/?next=/users/profile/')


@override_settings(LANGUAGE_CODE='en')
class TestProfileEdit(TestCase):

    fixtures = ['stud_auth_test_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('user_profile_edit')

    def test_access(self):
        response = self.client.get(self.url, follow=True)
        # status code 200
        self.assertEqual(response.status_code, 200)
        # login page
        self.assertIn('Log in', response.content)
        # right link
        self.assertEqual(response.redirect_chain[0][0],
             'http://testserver/users/login/?next=/users/profile/edit/')


@override_settings(LANGUAGE_CODE='en')
class TestRegistrationForm(TestCase):

    fixtures = ['stud_auth_test_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('registration_register')

    def test_get_form(self):
        response = self.client.get(self.url)

        ## title: 'Register Form'
        self.assertIn('Register Form', response.content)
        # form fields, 'Save' button
        self.assertIn('name="username"', response.content)
        self.assertIn('name="email"', response.content)
        self.assertIn('name="password1"', response.content)
        self.assertIn('name="password2"', response.content)
        self.assertIn('name="add_button"', response.content)

    def test_post_data(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(self.url,
                                    {'username': 'TestUser',
                                     'email': 'test@test.com',
                                     'password1': 'test',
                                     'password2': 'test'},
                                   follow=True)
        # check response status code
        self.assertEqual(response.status_code, 200)
        # right redirection
        self.assertEqual(response.redirect_chain[0][0],
                         'http://testserver/users/register/complete/')
        # new user in db
        self.assertEqual(User.objects.filter(
            username='TestUser',
            email='test@test.com').count(), 1)