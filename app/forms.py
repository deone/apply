from django import forms
from django.contrib.admin import widgets

from app.models import PersonalInformation

class PersonalInformationForm(forms.ModelForm):

    class Meta:
        model = PersonalInformation
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(PersonalInformationForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['middle_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['gender'].widget = forms.RadioSelect(choices=PersonalInformation.GENDER_CHOICES)
        self.fields['applied_before'].widget = forms.RadioSelect(choices=PersonalInformation.BOOL_CHOICES)
        self.fields['applied_before'].label = 'Have you applied to Ashesi before?'
        self.fields['year_applied'].widget = forms.TextInput(attrs={'class': 'form-control'})
