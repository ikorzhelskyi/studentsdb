from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse

from ..models import Group

@override_settings(LANGUAGE_CODE='en')
class TestGroupsList(TestCase):

    fixtures = ['students_test_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('groups')

    def test_access(self):
        response = self.client.get(self.url, follow=True)

        # we must have response status 200 and login page
        self.assertEqual(response.status_code, 200)
        self.assertIn('Log in', response.content)
        # check the redirection link
        self.assertEqual(response.redirect_chain[0][0],
             'http://testserver/users/login/?next=/groups/')

    def test_groups_list(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)

        # response status code must be 200
        self.assertEqual(response.status_code, 200)
        # title 'Groups List' and button 'Add Group' must be on page
        self.assertIn('Groups List', response.content)
        self.assertIn('Add Group', response.content)
        # check if we have exactly 3 groups on page
        self.assertEqual(len(response.context['groups']), 3)

    def test_pagination(self):
        # test page=2
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url, {'page': '2'})
        # check response status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['groups']), 1)
        self.assertIn('Group2', response.content)

    def test_reverse_order_by(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url,
                   {'order_by': 'leader', 'reverse': '1'})
        # check response status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['groups']), 3)
        self.assertIn('Student1 Last Name 1', response.content)

    def test_current_group(self):
        group = Group.objects.get(id=1)
        self.client.login(username='admin', password='admin')
        self.client.cookies['current_group'] = group.id
        response = self.client.get(self.url)
        # do we got only one selected group on the page?
        self.assertEqual(len(response.context['groups']), 1)
        self.assertIn('Group1', response.content)


@override_settings(LANGUAGE_CODE='en')
class TestGroupAdd(TestCase):

    fixtures = ['students_test_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('groups_add')

    def test_access(self):
        response = self.client.get(self.url, follow=True)

        # we must have response status 200 and login page
        self.assertEqual(response.status_code, 200)
        self.assertIn('Log in', response.content)
        # check the redirection link
        self.assertEqual(response.redirect_chain[0][0],
             'http://testserver/users/login/?next=/groups/add/')

    def test_get_form(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)

        # response status code must be 200
        self.assertEqual(response.status_code, 200)
        # page must contain page title and form with 'action' attr
        self.assertIn('Group Form', response.content)
        self.assertIn('action="/groups/add/"', response.content)
        self.assertIn('name="title"', response.content)
        self.assertIn('name="leader"', response.content)
        self.assertIn('name="add_button"', response.content)

    def test_post_wrong_data(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(self.url,
                                    {'title': '',
                                     'leader': ''},
                                    follow=True)

        # response status code must be 200
        self.assertEqual(response.status_code, 200)
        # form must contain error message
        self.assertIn('This field is required', response.content)

    def test_post_right_data(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(self.url,
                                    {'title': 'New Group',
                                     'leader': ''},
                                    follow=True)

        # response status code must be 200
        self.assertEqual(response.status_code, 200)
        # check right redirection to 'groups' page
        self.assertEqual(response.redirect_chain[0][0],
                         'http://testserver/groups/?status_message=Changes%20saved%20successfully!')
        # check message "group created successfully"
        self.assertIn('Changes saved successfully!',
                      response.content)
        # check new group exists in db
        self.assertEqual(len(Group.objects.filter(title='New Group')), 1)

@override_settings(LANGUAGE_CODE='en')
class TestGroupUpdate(TestCase):

    fixtures = ['students_test_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('groups_edit', kwargs={'pk': '1'})

    def test_access(self):
        response = self.client.get(self.url, follow=True)

        # we must have response status 200 and login page
        self.assertEqual(response.status_code, 200)
        self.assertIn('Log in', response.content)
        # check the redirection link
        self.assertEqual(response.redirect_chain[0][0],
             'http://testserver/users/login/?next=/groups/1/edit/')

    def test_get_form(self):
        group = Group.objects.get(id=1)

        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)

        # response status code must be 200
        self.assertEqual(response.status_code, 200)
        # page must contain page title and form with 'action' attr
        self.assertIn('Group Form', response.content)
        self.assertIn('action="/groups/1/edit/"', response.content)
        self.assertIn('name="title"', response.content)
        self.assertIn('name="leader"', response.content)
        self.assertIn('name="save_button"', response.content)
        # form must be filled with data
        self.assertIn(group.title, response.content.decode('utf-8'))
        self.assertIn(unicode(group.leader), response.content.decode('utf-8'))

    def test_post_wrong_data(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(self.url,
                                    {'title': '',
                                     'leader': ''},
                                    follow=True)

        # response status code must be 200
        self.assertEqual(response.status_code, 200)
        # form must contain error message
        self.assertIn('This field is required', response.content)

    def test_post_right_data(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(self.url,
                                    {'title': 'New Group1',
                                     'leader': '1'},
                                    follow=True)

        # response status code must be 200
        self.assertEqual(response.status_code, 200)
        # check right redirection to 'groups' page
        self.assertEqual(response.redirect_chain[0][0],
                         'http://testserver/groups/?status_message=Changes%20saved%20successfully!')
        # check message about group saving
        self.assertIn('Changes saved successfully!',
                      response.content)
        # check updated group exists in db
        self.assertEqual(len(Group.objects.filter(
            title='New Group1',
            leader__id=1,)), 1)


@override_settings(LANGUAGE_CODE='en')
class TestGroupDelete(TestCase):

    fixtures = ['students_test_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('groups_delete', kwargs={'pk': '1'})

    def test_access(self):
        response = self.client.get(self.url, follow=True)

        # we must have response status 200 and login page
        self.assertEqual(response.status_code, 200)
        self.assertIn('Log in', response.content)
        # check the redirection link
        self.assertEqual(response.redirect_chain[0][0],
             'http://testserver/users/login/?next=/groups/1/delete/')
        # and same cheking for POST
        response = self.client.post(self.url, follow=True)
        # we must have response status 200 and login page
        self.assertEqual(response.status_code, 200)
        self.assertIn('Log in', response.content)
        # check the redirection link
        self.assertEqual(response.redirect_chain[0][0],
             'http://testserver/users/login/?next=/groups/1/delete/')

    def test_confirm_delete(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url, follow=True)

        # there must be confirmation page
        # with question and button in form
        self.assertIn('Do you really want to delete group',
                      response.content)
        self.assertIn('action="/groups/1/delete/"',
                      response.content)