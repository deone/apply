from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from setup.models import Organization, Application, UserApplication

class AppTest(TestCase):

    def setUp(self, *args, **kwargs):
        user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        user.first_name = 'Dayo'
        user.last_name = 'Osikoya'
        user.save()
        organization = Organization.objects.create(name='Ecobank Ghana', short_name='Ecobank')
        application = Application.objects.create(
            organization=organization,
            name='Account Opening Form',
            is_open=True,
            deadline=timezone.now()
            )
        self.user_app = UserApplication.objects.create(user=user, application=application)
