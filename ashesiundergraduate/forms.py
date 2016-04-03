from django import forms
from django.conf import settings
from django.contrib.admin import widgets

from .models import PersonalInformation
from setup.models import UserApplication

class PersonalInformationForm(forms.ModelForm):

    class Meta:
        model = PersonalInformation
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.application = kwargs.pop('application', None)
        super(PersonalInformationForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['date_of_birth'].input_formats = settings.DATE_INPUT_FORMATS
        self.fields['middle_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['gender'].widget = forms.RadioSelect(choices=PersonalInformation.GENDER_CHOICES)
        self.fields['applied_before'].widget = forms.RadioSelect(choices=PersonalInformation.BOOL_CHOICES)
        self.fields['applied_before'].label = 'Have you applied to Ashesi before?'
        self.fields['year_applied'].widget = forms.TextInput(attrs={'class': 'form-control'})

    def save(self):
        user_application = UserApplication.objects.get(application=self.application, user=self.user)
        return PersonalInformation.objects.create(
            user_application=user_application,
            middle_name=self.cleaned_data['middle_name'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            gender=self.cleaned_data['gender'],
            applied_before=self.cleaned_data['applied_before'],
            year_applied=self.cleaned_data['year_applied']
            )
