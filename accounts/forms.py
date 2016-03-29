from django import forms

from registration.forms import RegistrationForm

class ApplyRegistrationForm(RegistrationForm):

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    def __init__(self, *args, **kwargs):
        super(ApplyRegistrationForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')

    def save(self):
        self.instance.username = self.cleaned_data['email']
        return super(ApplyRegistrationForm, self).save()
