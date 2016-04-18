from ...models import Citizenship
from ...forms import CitizenshipForm

from . import FormsTest

class CitizenshipFormTest(FormsTest):

    def setUp(self, *args, **kwargs):
        super(CitizenshipFormTest, self).setUp(*args, **kwargs)
        self.data = {'country_of_citizenship': 'Nigeria'}

    def test_save_new(self):
        super(CitizenshipFormTest, self).form_test(CitizenshipForm, self.data, obj=self.user_app)

    def test_save_existing(self):
        Citizenship.objects.create(user_application=self.user_app, country_of_citizenship='Angola')
        super(CitizenshipFormTest, self).form_test(CitizenshipForm, self.data, obj=self.user_app)
