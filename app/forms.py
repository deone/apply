from django import forms

from app.models import PersonalInformation

class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        # exclude = ['middle_name']
        exclude = ['user']
