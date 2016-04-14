from django import forms

from utils.getters import get_obj_from_form

from ..models import Citizenship

class CitizenshipForm(forms.ModelForm):

    class Meta:
        model = Citizenship
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user_application = get_obj_from_form(kwargs)
        super(CitizenshipForm, self).__init__(*args, **kwargs)
        self.fields['country_of_citizenship'].widget = forms.TextInput(attrs={'class': 'form-control'})

    def save(self, commit=False):
        data = self.cleaned_data
        citizenship, created = Citizenship.objects.get_or_create(user_application=self.user_application, defaults=data)
        if not created:
            citizenship.country_of_citizenship = data['country_of_citizenship']
            citizenship.save()
            
        return citizenship
