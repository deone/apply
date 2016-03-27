from django import forms

from registration.forms import RegistrationForm

class ApplyRegistrationForm(RegistrationForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
