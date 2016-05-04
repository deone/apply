from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import *
from . import AppTest

class ModelsTest(AppTest):

    def setUp(self, *args, **kwargs):
        super(ModelsTest, self).setUp(*args, **kwargs)

    def test_personal_information(self):
        image = os.path.join(settings.BASE_DIR, 'ashesiundergraduate/tests/test_files/Dayo_Osikoya.jpg')
        data = {
            'user_application': self.user_app,
            'middle_name': 'J',
            'date_of_birth': '2012-01-01',
            'primary_phone_number': '+233542741720',
            'alternative_phone_number': '+233756890123',
            'applied_before': True,
            'year_applied': '1999',
            'gender': 'M',
            }
        with open(image) as image:
            image_name = image.name.split('/')[-1:][0]
            photo = {
                'photo': SimpleUploadedFile(image_name, image.read(), 'image/jpeg')
                }
        pi = PersonalInformation(**data)
        pi.save()
        self.assertEqual(pi.__str__(), 'Dayo J Osikoya')

    def test_citizenship(self):
        citizenship = Citizenship.objects.create(user_application=self.user_app, country_of_citizenship='Nigeria')
        self.assertEqual(citizenship.__str__(), 'Dayo Osikoya Nigeria')

    def test_passport_details(self):
        passport_check = PassportCheck.objects.create(user_application=self.user_app, have_passport=True)
        passport_details = PassportDetails.objects.create(passport_check=passport_check,
            passport_number='AAA1234567GH', expiry_date='2018-01-01')
        self.assertEqual(passport_check.__str__(), 'Dayo Osikoya True')
        self.assertEqual(passport_details.__str__(), 'AAA1234567GH')

    def test_residence(self):
        residence = Residence.objects.create(user_application=self.user_app,
            address='House 2', town='Labone', state='Accra', country='Ghana', living_with='ORPH')
        orphanage = Orphanage.objects.create(residence=residence, name='Bless God',
            contact_person_title='Manager', contact_person_name='Ade Olu', contact_person_phone_number='+233546723450',
            email='ade@gmail.com')
        self.assertEqual(residence.__str__(), 'Labone, Accra, Ghana')
        self.assertEqual(orphanage.__str__(), 'Bless God')

    def test_desired_major(self):
        course = Course.objects.create(name='Computer Science')
        desired_major = DesiredMajor.objects.create(user_application=self.user_app, desired_major=course)
        self.assertEqual(course.__str__(), 'Computer Science')
        self.assertEqual(desired_major.__str__(), course.name)
