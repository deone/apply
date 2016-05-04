from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from ...models import PersonalInformation
from ...forms import PersonalInformationForm

from . import FormsTest

import os

class PersonalInformationFormTest(FormsTest):

    def setUp(self, *args, **kwargs):
        super(PersonalInformationFormTest, self).setUp(*args, **kwargs)
        self.image = os.path.join(settings.BASE_DIR, 'ashesiundergraduate/tests/test_files/Dayo_Osikoya.jpg')
        self.data = {
            'middle_name': 'J',
            'date_of_birth': '01-01-2012',
            'primary_phone_number': '+233542741720',
            'alternative_phone_number': '+233756890123',
            'applied_before': True,
            'year_applied': '1999',
            'gender': 'M',
            }
        with open(self.image) as image:
            image_name = image.name.split('/')[-1:][0]
            self.photo = {
                'photo': SimpleUploadedFile(image_name, image.read(), 'image/jpeg')
                }

    def test_save_new(self):
        obj = super(PersonalInformationFormTest, self).save_form(PersonalInformationForm, self.data, files=self.photo, obj=self.user_app)
        del obj['photo']
        self.assertEqual(obj, self.data)

    def test_save_existing(self):
        data = self.data.copy()
        data.update(self.photo)
        data.update({
          'user_application': self.user_app,
          'middle_name': 'Joshua',
          'applied_before': False,
          'year_applied': '',
          'date_of_birth': '2004-03-01',
          'alternative_phone_number': '',
          'photo': File(open(self.image)),
          })
        pi = PersonalInformation(**data)
        pi.save()
        obj = super(PersonalInformationFormTest, self).save_form(PersonalInformationForm, self.data, files=self.photo, obj=self.user_app)
        del obj['photo']
        self.assertEqual(obj, self.data)

    def test_applied_before_true_year_applied_empty(self):
        data = self.data.copy()
        data.update({'year_applied': ''})
        errors = super(PersonalInformationFormTest, self).save_form(PersonalInformationForm, data, files=self.photo, obj=self.user_app)
        self.assertTrue(errors['year_applied'].__contains__('Please specify the year you applied.'))

    def test_applied_before_false(self):
        data = self.data.copy()
        data.update({
          'year_applied': '2000',
          'applied_before': False,
          })
        obj = super(PersonalInformationFormTest, self).save_form(PersonalInformationForm, data, files=self.photo, obj=self.user_app)
        self.assertEqual(obj['year_applied'], '')
