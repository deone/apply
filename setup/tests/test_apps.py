from django.test import SimpleTestCase
from django.apps import apps

from ..apps import SetupConfig 

class TestApp(SimpleTestCase):

    def test(self):
        config = apps.get_app_config('setup')
        self.assertEqual(config.name, 'setup')
