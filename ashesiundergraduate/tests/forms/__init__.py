from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from setup.models import Organization, Application, UserApplication

class FormsTest(TestCase):

    def setUp(self, *args, **kwargs):
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
