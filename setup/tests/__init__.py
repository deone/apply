from django.test import TestCase
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

from setup.models import *

class AppTest(TestCase):

    def setUp(self, *args, **kwargs):
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        self.user.first_name = 'Dayo'
        self.user.last_name = 'Osikoya'
        self.user.save()
        self.organization = Organization.objects.create(name='Ashesi College', slug='ashesi')
        self.application = Application.objects.create(
            organization=self.organization,
            name='Undergraduate Application',
            year='2016',
            is_open=True
            )
        self.user_app = UserApplication.objects.create(user=self.user, application=self.application)
        self.form = Form.objects.create(name='Residence')
        self.app_form = ApplicationForm.objects.create(application=self.application, slug='residence', form=self.form)
