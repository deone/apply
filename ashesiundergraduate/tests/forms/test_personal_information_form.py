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
        settings.MEDIA_ROOT = '/Users/deone/src/apply/apply/ashesiundergraduate/tests/test_files/'
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
        super(PersonalInformationFormTest, self).form_test(PersonalInformationForm, self.data, files=self.photo, obj=self.user_app)

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
        super(PersonalInformationFormTest, self).form_test(PersonalInformationForm, self.data, files=self.photo, obj=self.user_app)
