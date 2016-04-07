from django import forms

from utils.getters import get_user_app_from_form

from ..models import Citizenship

class CitizenshipForm(forms.ModelForm):

    class Meta:
        model = Citizenship
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user_application = get_user_app_from_form(kwargs)
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
