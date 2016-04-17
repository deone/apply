from ...models import Citizenship
from ...forms import CitizenshipForm

from . import FormsTest

class CitizenshipFormTest(FormsTest):

    def setUp(self, *args, **kwargs):
        super(CitizenshipFormTest, self).setUp(*args, **kwargs)

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
