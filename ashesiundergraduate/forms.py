from django import forms
from django.conf import settings
from django.contrib.admin import widgets

from .models import *
from setup.models import UserApplication
from utils.getters import get_user_application

class PersonalInformationForm(forms.ModelForm):

    class Meta:
        model = PersonalInformation
        exclude = ['user_application', 'photo_height', 'photo_width']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        application = kwargs.pop('application', None)
        self.user_application = get_user_application(user=user, application=application)
        super(PersonalInformationForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['date_of_birth'].input_formats = settings.DATE_INPUT_FORMATS
        self.fields['middle_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['gender'].widget = forms.RadioSelect(choices=PersonalInformation.GENDER_CHOICES)
        self.fields['applied_before'].widget = forms.RadioSelect(choices=PersonalInformation.BOOL_CHOICES)
        self.fields['applied_before'].label = 'Have you applied to Ashesi before?'
        self.fields['year_applied'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['year_applied'].required = False
        self.fields['photo'].label = 'Passport-sized Photo'

    def clean_year_applied(self):
        if self.cleaned_data['applied_before'] == True and self.cleaned_data['year_applied'] == '':
            raise forms.ValidationError("Please specify the year you applied.")

        if self.cleaned_data['applied_before'] == False:
            self.cleaned_data['year_applied'] = ''

        return self.cleaned_data['year_applied']

    def clean_photo(self):
        if self.cleaned_data['photo'].name.split('.')[0] != '%s_%s' % (self.user_application.user.first_name.title(),
            self.user_application.user.last_name.title()):
            raise forms.ValidationError("Please rename your photo to conform with specified format.")
            
        return self.cleaned_data['photo']

    def save(self):
        data = self.cleaned_data
        try:
            personal_information = PersonalInformation.objects.get(user_application=self.user_application)
        except PersonalInformation.DoesNotExist:
            data.update({'user_application': self.user_application})
            personal_information = PersonalInformation(**data)
            personal_information.save()
        else:
            PersonalInformation.objects.filter(user_application=self.user_application).update(**data)

        return personal_information


class ScholarshipsForm(forms.ModelForm):

    class Meta:
        model = Scholarships
        exclude = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.application = kwargs.pop('application', None)
        super(ScholarshipsForm, self).__init__(*args, **kwargs)
