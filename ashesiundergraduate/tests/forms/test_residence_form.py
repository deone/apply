from ...models import Residence, Orphanage
from ...forms import ResidenceForm

from . import FormsTest

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
        super(ResidenceFormTest, self).form_test(ResidenceForm, self.data, obj=self.user_app)

    def test_save_existing(self):
        data = self.data.copy()
        data.update({'address': 'House 10', 'living_with': 'SELF', 'user_application': self.user_app})
        r = Residence(**data)
        r.save()

        super(ResidenceFormTest, self).form_test(ResidenceForm, self.data, obj=self.user_app)
