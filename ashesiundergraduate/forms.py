from django import forms
from django.conf import settings
from django.contrib.admin import widgets
from django.utils.translation import ugettext_lazy as _

from setup.models import UserApplication

from .models import *

class PersonalInformationForm(forms.ModelForm):

    class Meta:
        model = PersonalInformation
        exclude = ['user_application', 'photo_height', 'photo_width']

    def __init__(self, *args, **kwargs):
        self.user_application = kwargs.pop('user_application', None)
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
            raise forms.ValidationError(_("Please specify the year you applied."), code='year-not-specified')

        if self.cleaned_data['applied_before'] == False:
            self.cleaned_data['year_applied'] = ''

        return self.cleaned_data['year_applied']

    def clean_photo(self):
        file_name = self.cleaned_data['photo'].name.split('/')[-1]
        user = self.user_application.user
        user_name = '%s_%s' % (user.first_name.title(), user.last_name.title())
        if not file_name.startswith(user_name):
            raise forms.ValidationError(_("Please rename your photo to conform with specified format."), code='photo-name-error')
            
        return self.cleaned_data['photo']

    def save(self):
        data = self.cleaned_data
        try:
            personal_information = PersonalInformation.objects.get(user_application=self.user_application)
        except PersonalInformation.DoesNotExist:
            data.update({'user_application': self.user_application})
            personal_information = PersonalInformation(**data)
        else:
            personal_information.middle_name = data['middle_name']
            personal_information.date_of_birth = data['date_of_birth']
            personal_information.photo = data['photo']
            personal_information.gender = data['gender']
            personal_information.applied_before = data['applied_before']
            personal_information.year_applied = data['year_applied']

        personal_information.save()
        return personal_information

class CitizenshipForm(forms.ModelForm):

    class Meta:
        model = Citizenship
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user_application = kwargs.pop('user_application', None)
        super(CitizenshipForm, self).__init__(*args, **kwargs)
        self.fields['country_of_citizenship'].widget = forms.TextInput(attrs={'class': 'form-control'})

    def save(self):
        data = self.cleaned_data
        try:
            citizenship = Citizenship.objects.get(user_application=self.user_application)
        except Citizenship.DoesNotExist:
            data.update({'user_application': self.user_application})
            citizenship = Citizenship(**data)
        else:
            citizenship.country_of_citizenship = data['country_of_citizenship']

        citizenship.save()
        return citizenship

class ScholarshipsForm(forms.ModelForm):

    class Meta:
        model = Scholarships
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user_application = kwargs.pop('user_application', None)
        super(ScholarshipsForm, self).__init__(*args, **kwargs)
