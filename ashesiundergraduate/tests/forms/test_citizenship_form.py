from ...models import Citizenship
from ...forms import CitizenshipForm

from . import FormsTest, bind_save_form

class CitizenshipFormTest(FormsTest):

    def setUp(self, *args, **kwargs):
        super(CitizenshipFormTest, self).setUp(*args, **kwargs)
        self.data = {'country_of_citizenship': 'Nigeria'}

    def _assert(self, value):
        self.assertEqual(value, self.data['country_of_citizenship'])

    def test_save_new(self):
        citizenship = bind_save_form(CitizenshipForm, self.data, obj=self.user_app)
        self._assert(citizenship.country_of_citizenship)

    def test_save_existing(self):
        Citizenship.objects.create(user_application=self.user_app, country_of_citizenship='Angola')
        citizenship = bind_save_form(CitizenshipForm, self.data, obj=self.user_app)
        self._assert(citizenship.country_of_citizenship)
