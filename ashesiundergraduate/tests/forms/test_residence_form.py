from ...models import Residence, Orphanage
from ...forms import ResidenceForm, OrphanageForm

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
        super(ResidenceFormTest, self).save_form(ResidenceForm, self.data, obj=self.user_app)

    def test_save_existing(self):
        data = self.data.copy()
        data.update({'address': 'House 10', 'living_with': 'SELF', 'user_application': self.user_app})
        r = Residence(**data)
        r.save()

        obj = super(ResidenceFormTest, self).save_form(ResidenceForm, self.data, obj=self.user_app)
        self.assertEqual(obj, self.data)

class OrphanageFormTest(FormsTest):

    def setUp(self, *args, **kwargs):
        super(OrphanageFormTest, self).setUp(*args, **kwargs)
        self.residence_data = {
            'address': 'House 2',
            'town': 'Labone',
            'state': 'Accra',
            'country': 'Ghana',
            'living_with': 'ORPH',
            'user_application': self.user_app
            }
        self.residence = Residence(**self.residence_data)
        self.residence.save()
        self.data = {
            'name': 'Bless God Orphanage',
            'contact_person_name': 'Ade',
            'contact_person_title': 'Manager',
            'contact_person_phone_number': '+233542751610',
            'email': 'ade@blessgod.com'
            }

    def test_save_new(self):
        obj = super(OrphanageFormTest, self).save_form(OrphanageForm, self.data, parent=self.residence)
        self.assertEqual(obj, self.data)

    def test_save_existing(self):
        data = self.data.copy()
        data.update({'contact_person_title': 'CEO', 'contact_person_name': 'Olu', 'residence': self.residence})
        orph = Orphanage(**data)
        orph.save()

        obj = super(OrphanageFormTest, self).save_form(OrphanageForm, self.data, parent=self.residence)
        self.assertEqual(obj, self.data)

    def test_residence_living_with_not_orphanage(self):
        residence_data = self.residence_data.copy()
        residence_data.update({'living_with': 'PG'})

        super(OrphanageFormTest, self).form_test_without_bound_parent_form(ResidenceForm,
            OrphanageForm, residence_data, self.data, obj=self.user_app)
