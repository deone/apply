from django.test import SimpleTestCase
from django.apps import apps

from ..apps import AshesiundergraduateConfig

class TestApp(SimpleTestCase):

    def test(self):
        config = apps.get_app_config('ashesiundergraduate')
        self.assertEqual(config.name, 'ashesiundergraduate')
