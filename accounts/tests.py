from django.test import TestCase

from accounts.forms import ApplyRegistrationForm

class AccountsFormsTest(TestCase):

    def test_save(self):
        data = {'password1': '1234bbbb', 'password2': '1234bbbb', 'last_name': 'Osikoya', 'email': 'a@a.com', 'first_name': 'Dayo'}
        form = ApplyRegistrationForm(data)
        if form.is_valid():
            instance = form.save()

        self.assertEqual(instance.username, data['email'])
