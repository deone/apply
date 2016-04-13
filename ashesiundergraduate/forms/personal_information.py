from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from utils.getters import get_obj_from_form

from ..models import PersonalInformation

class PersonalInformationForm(forms.ModelForm):

    class Meta:
        model = PersonalInformation
        exclude = ['user_application', 'photo_height', 'photo_width']

    def __init__(self, *args, **kwargs):
        self.user_application = get_obj_from_form(kwargs)
        super(PersonalInformationForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = forms.TextInput(attrs={'class': 'form-control date'})
        self.fields['date_of_birth'].input_formats = settings.DATE_INPUT_FORMATS
        self.fields['middle_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['primary_phone_number'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['alternative_phone_number'].widget = forms.TextInput(attrs={'class': 'form-control'})
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
        personal_information, created = PersonalInformation.objects.get_or_create(user_application=self.user_application,
            defaults=data)
        if not created:
            personal_information.middle_name = data['middle_name']
            personal_information.date_of_birth = data['date_of_birth']
            personal_information.photo = data['photo']
            personal_information.gender = data['gender']
            personal_information.applied_before = data['applied_before']
            personal_information.year_applied = data['year_applied']
            personal_information.save()

        return personal_information
