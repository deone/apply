from django import forms

from registration.forms import RegistrationForm

class ApplyRegistrationForm(RegistrationForm):

    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ApplyRegistrationForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

    def save(self, commit=False):
        self.instance.username = self.cleaned_data['email']
        return super(ApplyRegistrationForm, self).save()
