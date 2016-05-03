from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sites.models import Site

from setup.models import *
from payments.models import Payment
from utils.getters import get_user_application

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

    # @override_settings(SITE_ID=2)
    def test_application_index(self):
        # site = Site.objects.get(pk=1)
        # print site.name, site.domain
        # site.pk = settings.SITE_ID
        # site.save()
        # print site.name, site.domain, site.pk

        # current_site = Site.objects.get_current()
        # print current_site.name
        # self.assertEqual(current_site.name, 'Apply Central Demo')

        self.c.post(reverse('login'), {'username': 'a@a.com', 'password': '12345'})
        response = self.c.get(reverse('application', kwargs={'orgname': self.org.slug, 'slug': self.application.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ashesiundergraduate/index.html')

    def test_application_index_insert_payment_record(self):
        self.application.has_fee = True
        self.application.fee = 10
        self.application.save()

        self.c.post(reverse('login'), {'username': 'a@a.com', 'password': '12345'})
        url = '%s?token=kdfhdfldf' % reverse('application', kwargs={'orgname': self.org.slug, 'slug': self.application.slug})
        response = self.c.get(url)

        user_application = self.application.userapplication_set.all()[0]
        payment = Payment.objects.get(user_application=user_application)

        self.assertEqual(payment.token, 'kdfhdfldf')
        self.assertEqual(response.status_code, 302)

    def test_success(self):
        self.c.post(reverse('login'), {'username': 'a@a.com', 'password': '12345'})
        response = self.c.get(reverse('success', kwargs={'orgname': self.org.slug, 'slug': self.application.slug}))

        user_application = self.application.userapplication_set.all()[0]

        self.assertTrue(user_application.is_complete)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ashesiundergraduate/success.html')
