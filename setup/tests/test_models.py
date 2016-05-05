from ..models import *
from . import AppTest

class ModelsTest(AppTest):

    def test_organization(self):
        self.assertEqual(self.organization.__str__(), 'Ashesi College')

    def test_staff(self):
        staff = Staff.objects.create(user=self.user, organization=self.organization)
        self.assertEqual(staff.__str__(), 'Dayo Osikoya')
