from django.test import TestCase, SimpleTestCase
from django.apps import apps

from .apps import AccountsConfig

from accounts.forms import ApplyRegistrationForm

class TestApp(SimpleTestCase):

    def test(self):
        config = apps.get_app_config('accounts')
        self.assertEqual(config.name, 'accounts')

class AccountsFormsTest(TestCase):

    def test_save(self):
        data = {'password1': '1234bbbb', 'password2': '1234bbbb', 'last_name': 'Osikoya', 'email': 'a@a.com', 'first_name': 'Dayo'}
        form = ApplyRegistrationForm(data)
        if form.is_valid():
            instance = form.save()

        self.assertEqual(instance.username, data['email'])
