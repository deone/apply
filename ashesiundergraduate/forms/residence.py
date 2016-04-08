from django import forms
from django.utils.translation import ugettext_lazy as _

from utils.getters import get_user_app_from_form

from ..models import Residence

class ResidenceForm(forms.ModelForm):

    class Meta:
        model = Residence
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user_application = get_user_app_from_form(kwargs)
        super(ResidenceForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['town'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['state'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['country'].widget = forms.TextInput(attrs={'class': 'form-control'})
