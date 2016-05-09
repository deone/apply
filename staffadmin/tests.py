from django.test import TestCase, SimpleTestCase
from django.core.urlresolvers import reverse

from setup.tests.views.tests import ViewsTests

from django.test import SimpleTestCase
from django.apps import apps

from .apps import StaffadminConfig 

class TestApp(SimpleTestCase):

    def test(self):
        config = apps.get_app_config('staffadmin')
        self.assertEqual(config.name, 'staffadmin')

class StaffadminViewsTests(ViewsTests):

    def test_index(self):
        self.login()
        response = self.c.get(reverse('staffadmin:home', kwargs={'orgname': 'ashesi'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staffadmin/index.html')

    def test_user_application(self):
        self.login()
        response = self.c.get(reverse('staffadmin:user_application', kwargs={'orgname': 'ashesi', 'pk': self.user_app.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user_application' in response.context)
        self.assertTemplateUsed(response, 'ashesiundergraduate/user_application.html')

    def test_user_application_list(self):
        self.login()
        response = self.c.get(reverse('staffadmin:user_application_list', kwargs={'orgname': 'ashesi', 'pk': self.application.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('application' in response.context)
        self.assertTemplateUsed(response, 'staffadmin/user_application_list.html')
