from ..models import *
from . import AppTest

class ModelsTest(AppTest):

    def test_organization(self):
        self.assertEqual(self.organization.__str__(), 'Ashesi College')

    def test_staff(self):
        staff = Staff.objects.create(user=self.user, organization=self.organization)
        self.assertEqual(staff.__str__(), 'Dayo Osikoya')

    def test_application_without_year(self):
        application = Application.objects.create(
            organization=self.organization,
            name='Undergraduate Application',
            is_open=True
            )

        self.assertEqual(application.__str__(), 'Ashesi College Undergraduate Application')

    def test_form(self):
        self.assertEqual(self.form.__str__(), 'Residence')

    def test_application_form(self):
        self.assertEqual(self.app_form.__str__(), 'Ashesi College Undergraduate Application 2016 Residence')

    def test_user_application(self):
        self.assertEqual(self.user_app.__str__(), 'Dayo Osikoya Ashesi College Undergraduate Application 2016')

    def test_saved_form(self):
        sf = SavedForm.objects.create(user_application=self.user_app, form_slug='residence')
        self.assertEqual(sf.__str__(), 'Undergraduate Application 2016 residence')
