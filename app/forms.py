from django import forms
from django.contrib.admin import widgets

from app.models import PersonalInformation

class PersonalInformationForm(forms.ModelForm):

    class Meta:
        model = PersonalInformation
        exclude = ['user', 'middle_name']

    def __init__(self, *args, **kwargs):
        super(PersonalInformationForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['gender'].widget = forms.RadioSelect(choices=PersonalInformation.GENDER_CHOICES)
