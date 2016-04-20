from ...models import PassportCheck, PassportDetails
from ...forms import PassportCheckForm, PassportDetailsFormSet

from . import FormsTest

class PassportCheckFormTest(FormsTest):

    def setUp(self, *args, **kwargs):
        super(PassportCheckFormTest, self).setUp(*args, **kwargs)
        self.data = {'have_passport': True}

    def test_save_new(self):
        super(PassportCheckFormTest, self).form_test(PassportCheckForm, self.data, obj=self.user_app)

    def test_save_existing(self):
        PassportCheck.objects.create(user_application=self.user_app, have_passport=False)
        super(PassportCheckFormTest, self).form_test(PassportCheckForm, self.data, obj=self.user_app)


class PassportDetailsFormSetTest(FormsTest):

    def setUp(self, *args, **kwargs):
        super(PassportDetailsFormSetTest, self).setUp(*args, **kwargs)
        self.passport_check_data = {
            'have_passport': True,
            'user_application': self.user_app
            }
        self.passport_check = PassportCheck(**self.passport_check_data)
        self.passport_check.save()
        self.data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '2',
            'form-0-passport_number': '11BB456NG',
            'form-0-expiry_date': '01-08-2017',
            'form-1-passport_number': '11BB456YY',
            'form-1-expiry_date': '01-08-2018'
            }

    def test_save_new(self):
        formset = PassportDetailsFormSet(self.data, obj=self.passport_check)
        if formset.is_valid():
            instances = formset.save(self.passport_check)
        self.assertEqual(instances[0].passport_number, self.data['form-0-passport_number'])
        self.assertEqual(instances[1].passport_number, self.data['form-1-passport_number'])

    def test_passport_check_have_passport_false(self):
        passport_check_data = self.passport_check_data.copy()
        passport_check_data.update({'have_passport': False})

        super(PassportDetailsFormSetTest, self).form_test_without_bound_parent_form(PassportCheckForm,
            PassportDetailsFormSet, passport_check_data, self.data, obj=self.user_app)
