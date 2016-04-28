from django import forms
from django.utils.translation import ugettext_lazy as _

from utils.getters import get_obj_from_form

from ..models import Residence, Orphanage
from utils import validate_phone_number

class ResidenceForm(forms.ModelForm):

    class Meta:
        model = Residence
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user_application = get_obj_from_form(kwargs)
        super(ResidenceForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['town'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['state'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['country'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['living_with'] = forms.ChoiceField(label='Who do you live with?', choices=Residence.LIVING_WITH_CHOICES,
            widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        if commit is False:
            return super(ResidenceForm, self).save(commit=False)
        else:
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
        self.residence = get_obj_from_form(kwargs)
        # kwarg obj is set to None if request is GET
        if self.residence is not None:
            # this is executed only if request is POST
            # form is initialized only if the main form determining field is a specific value
            # this ensures that we only attempt binding and validating the dependent form if that value is set
            # if the value is not set, return prematurely. This will throw an AttributeError upon validation since is_bound is not set on the form
            if self.residence.living_with != 'ORPH':
                return
        super(OrphanageForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['contact_person_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['contact_person_title'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['contact_person_phone_number'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'form-control'})

    def clean_contact_person_phone_number(self):
        number = self.cleaned_data['contact_person_phone_number']
        validate_phone_number(number)

        return number

    def save(self, residence):
        data = self.cleaned_data
        orphanage, created = Orphanage.objects.get_or_create(residence=residence, defaults=data)
        if not created:
            orphanage.name = data['name']
            orphanage.contact_person_name = data['contact_person_name']
            orphanage.contact_person_title = data['contact_person_title']
            orphanage.contact_person_phone_number = data['contact_person_phone_number']
            orphanage.email = data['email']
            orphanage.save()

        return orphanage
