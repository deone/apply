from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from setup.models import *

class ViewsTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        self.user.first_name = 'Ade'
        self.user.last_name = 'Olu'
        self.user.save()

class HomePageTests(ViewsTests):

    def test_applicant_home(self):
        self.c.post(reverse('login'), {'username': 'a@a.com', 'password': '12345'})
        response = self.c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('applications' in response.context)
        self.assertTemplateUsed(response, 'setup/application_list.html')

class ApplicationTests(ViewsTests):

    def setUp(self, *args, **kwargs):
        super(ApplicationTests, self).setUp(*args, **kwargs)
        self.org = Organization.objects.create(name='Ashesi College', slug='ashesi')
        self.staff = Staff.objects.create(user=self.user, organization=self.org)
        self.application = Application.objects.create(
            organization=self.org,
            name='Undergraduate Application',
            year='2016',
            is_open=True
            )
        form = Form.objects.create(name='Personal Information')
        application_form = ApplicationForm.objects.create(application=self.application, slug='personal-information', form=form)

    def test_applicant_home_staff(self):
        self.c.post(reverse('login'), {'username': 'a@a.com', 'password': '12345'})
        response = self.c.get(reverse('home'))
        self.assertEqual(response['location'], '/ashesi/admin/')
        self.assertEqual(response.status_code, 302)

    def test_application_index(self):
        self.c.post(reverse('login'), {'username': 'a@a.com', 'password': '12345'})
        response = self.c.get(reverse('application', kwargs={'orgname': self.org.slug, 'slug': self.application.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ashesiundergraduate/index.html')
