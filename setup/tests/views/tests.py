from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from setup.models import Organization, Staff

class ViewsTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')

    def test_applicant_home(self):
        self.c.post(reverse('login'), {'username': 'a@a.com', 'password': '12345'})
        response = self.c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('applications' in response.context)
        self.assertTemplateUsed(response, 'setup/application_list.html')

    def test_applicant_home_staff(self):
        org = Organization.objects.create(name='Ashesi College', slug='ashesi')
        staff = Staff.objects.create(user=self.user, organization=org)

        self.c.post(reverse('login'), {'username': 'a@a.com', 'password': '12345'})
        response = self.c.get(reverse('home'))
        self.assertEqual(response['location'], '/ashesi/admin/')
        self.assertEqual(response.status_code, 302)
