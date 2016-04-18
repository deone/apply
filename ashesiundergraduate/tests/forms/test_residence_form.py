from ...models import Residence, Orphanage
from ...forms import ResidenceForm

from . import FormsTest, bind_save_form

class ResidenceFormTest(FormsTest):
    
    def setUp(self, *args, **kwargs):
        super(ResidenceFormTest, self).setUp(*args, **kwargs)
        self.data = {
            'address': 'House 2',
            'town': 'Labone',
            'state': 'Accra',
            'country': 'Ghana',
            'living_with': 'PG'
            }

    def test_save_new(self):
        residence = bind_save_form(ResidenceForm, self.data, obj=self.user_app)
        self.assertEqual(residence.to_dict(), self.data)

    def test_save_existing(self):
        data = self.data.copy()
        data.update({'address': 'House 10', 'living_with': 'SELF', 'user_application': self.user_app})
        r = Residence(**data)
        r.save()

        residence = bind_save_form(ResidenceForm, self.data, obj=self.user_app)
        self.assertEqual(residence.to_dict(), self.data)
