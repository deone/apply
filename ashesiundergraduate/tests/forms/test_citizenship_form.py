from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from setup.models import Organization, Application, UserApplication

from ...models import Citizenship
from ...forms import CitizenshipForm

class CitizenshipFormTest(TestCase):

    def setUp(self, *args, **kwargs):
        super(CitizenshipFormTest, self).setUp(*args, **kwargs)
        self.data = {'country_of_citizenship': 'Nigeria'}
        user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        organization = Organization.objects.create(name='Ecobank Ghana', short_name='Ecobank')
        application = Application.objects.create(
            organization=organization,
            name='Account Opening Form',
            is_open=True,
            deadline=timezone.now()
            )
        self.user_app = UserApplication.objects.create(user=user, application=application)

    def test_save_new(self):
        form = CitizenshipForm(self.data, obj=self.user_app)
        form.is_valid()
        citizenship = form.save()
        
        self.assertEqual(citizenship.country_of_citizenship, 'Nigeria')

    def test_save_existing(self):
        citizenship = Citizenship.objects.create(user_application=self.user_app, country_of_citizenship='Angola')
        form = CitizenshipForm(self.data, obj=self.user_app)
        form.is_valid()
        citizenship = form.save()

        self.assertEqual(citizenship.country_of_citizenship, 'Nigeria')
