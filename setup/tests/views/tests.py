from django.test import TestCase, Client, RequestFactory, override_settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages

from setup.models import *
from setup.views import application_form
from payments.models import Payment
from utils.getters import get_user_application, get_next_form_slug, get_initial_data
from ashesiundergraduate.models import Citizenship

class ViewsTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        self.user.first_name = 'Ade'
        self.user.last_name = 'Olu'
        self.user.save()

    def login(self):
        self.c.post(reverse('login'), {'username': 'a@a.com', 'password': '12345'})

class HomePageTests(ViewsTests):

    def test_applicant_home(self):
        self.login()
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
        form = Form.objects.create(name='Residence')
        self.app_form = ApplicationForm.objects.create(application=self.application, slug='residence', form=form)

    def test_applicant_home_staff(self):
        self.login()
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

        self.login()
        response = self.c.get(reverse('application', kwargs={'orgname': self.org.slug, 'slug': self.application.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ashesiundergraduate/index.html')

    def test_application_index_insert_payment_record(self):
        self.application.has_fee = True
        self.application.fee = 10
        self.application.save()

        self.login()
        url = '%s?token=kdfhdfldf' % reverse('application', kwargs={'orgname': self.org.slug, 'slug': self.application.slug})
        response = self.c.get(url)

        user_application = self.application.userapplication_set.all()[0]
        payment = Payment.objects.get(user_application=user_application)

        self.assertEqual(payment.token, 'kdfhdfldf')
        self.assertEqual(response.status_code, 302)

    def test_success(self):
        self.login()
        response = self.c.get(reverse('success', kwargs={'orgname': self.org.slug, 'slug': self.application.slug}))

        user_application = self.application.userapplication_set.all()[0]

        self.assertTrue(user_application.is_complete)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ashesiundergraduate/success.html')

    def test_application_form_get(self):
        self.login()
        response = self.c.get(reverse('application_form', kwargs={
          'orgname': self.org.slug,
          'slug': self.application.slug,
          'form_slug': self.app_form.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue('form_name' in response.context)
        self.assertTrue('dep_form' in response.context)

class ApplicationFormTests(ApplicationTests):

    def setUp(self, *args, **kwargs):
        super(ApplicationFormTests, self).setUp(*args, **kwargs)
        self.factory = RequestFactory()
        self.session = SessionMiddleware()
        self.residence_data = {
              'address': 'Hse 2',
              'town': 'Lagos',
              'state': 'Lagos',
              'country': 'Nigeria',
              'living_with': 'SELF',
              }
        self.orphanage_data = {
              'name': 'Bless God',
              'email': 'b@b.com',
              'contact_person_name': 'Ade',
              'contact_person_phone_number': '+233542751610',
              'contact_person_title': 'Manager',
              }

    def test_application_form_with_main_form_only_invalid(self):
        self.login()
        form = Form.objects.create(name='Citizenship')
        app_form = ApplicationForm.objects.create(application=self.application, slug='citizenship', form=form)
        data = {
            'country_of_citizenship': ''
            }
        response, lst = self.application_form_test(app_form, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(lst, [])

    def test_application_form_with_main_form_only(self):
        self.login()
        form = Form.objects.create(name='Citizenship')
        app_form = ApplicationForm.objects.create(application=self.application, slug='citizenship', form=form)
        data = {
            'country_of_citizenship': 'Angola'
            }
        response, lst = self.application_form_test(app_form, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual('Citizenship saved.', lst[0].__str__())

    def test_application_form_with_main_form_null_dep_form(self):
        self.login()
        response, lst = self.application_form_test(self.app_form, self.residence_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual('Residence saved.', lst[0].__str__())

    def application_form_test(self, app_form, data):
        request = self.factory.post(reverse('application_form',
          kwargs={
              'orgname': self.org.slug,
              'slug': self.application.slug,
              'form_slug': app_form.slug
              }), data=data)

        request.user = self.user
        self.session.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = application_form(request, self.org.slug, self.application.slug, app_form.slug)
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        return response, lst

    def test_application_form_post_with_main_form_dep_form(self):
        self.login()
        data = self.residence_data
        data.update(self.orphanage_data)
        response, lst = self.application_form_test(self.app_form, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual('Residence saved.', lst[0].__str__())

    def test_get_next_form_slug(self):
        form_two = Form.objects.create(name='Passport Details')
        app_form_two = ApplicationForm.objects.create(application=self.application, slug='passport-details', form=form_two)
        next_slug = get_next_form_slug(self.application, 'residence')

        self.assertEqual(next_slug, 'passport-details')

    def create_object(self):
        user_app = get_user_application(self.user, self.application)
        data = {'country_of_citizenship': 'Angola', 'user_application': user_app}
        c = Citizenship(**data)
        c.save()

        return data, user_app

    def test_get_initial_data_form_type_form(self):
        data, user_app = self.create_object()
        initial_data, dep_data = get_initial_data('ashesiundergraduate', 'Citizenship', 'form', user_app, None)

        del data['user_application']

        self.assertEqual(initial_data, data)

    def test_get_initial_data_form_type_formset(self):
        data, user_app = self.create_object()
        initial_data, dep_data = get_initial_data('ashesiundergraduate', 'Citizenship', 'formset', user_app, None)

        self.assertEqual(initial_data, None)

    """ def test_get_initial_data_attr_obj_not_none(self):
        initial_data, dep_data = get_initial_data('ashesiundergraduate', 'Residence', 'form', user_app, 'orphanage') """
