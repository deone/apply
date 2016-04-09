from django import forms
from django.utils.translation import ugettext_lazy as _

from utils.getters import get_obj_from_form

from ..models import Residence, Orphanage

class ResidenceForm(forms.ModelForm):

    class Meta:
        model = Residence
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user_application = get_obj_from_form('user_application', kwargs)
        super(ResidenceForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['town'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['state'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['country'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['living_with'] = forms.ChoiceField(label='Who do you live with?', choices=Residence.LIVING_WITH_CHOICES,
            widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self):
        data = self.cleaned_data
        residence, created = Residence.objects.get_or_create(user_application=self.user_application, defaults=data)
        if not created:
            residence.address = data['address']
            residence.town = data['town']
            residence.state = data['state']
            residence.country = data['country']
            residence.living_with = data['living_with']
            residence.save()

        return residence

class OrphanageForm(forms.ModelForm):

    class Meta:
        model = Orphanage
        exclude = ['residence']

    def __init__(self, *args, **kwargs):
        self.residence = get_obj_from_form('residence', kwargs)
        super(OrphanageForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['contact_person_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['contact_person_title'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['contact_person_phone_number'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['contact_person_email'].widget = forms.TextInput(attrs={'class': 'form-control'})
