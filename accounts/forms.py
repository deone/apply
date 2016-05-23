from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm

from registration.forms import RegistrationForm

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label=_('Email'), max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ApplyRegistrationForm(RegistrationForm):

    first_name = forms.CharField(label=_('First Name'), widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label=_('Last Name'), widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ApplyRegistrationForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password1'].help_text = _('Password must contain at least 8 characters.')
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

    def save(self, commit=False):
        self.instance.username = self.cleaned_data['email']
        return super(ApplyRegistrationForm, self).save()

class ApplyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))
