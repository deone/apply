from django import forms

from utils.getters import get_user_app_from_form

from ..models import PassportDetails

class PassportDetailsForm(forms.ModelForm):

    class Meta:
        model = PassportDetails
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user_application = get_user_app_from_form(kwargs)
        super(PassportDetailsForm, self).__init__(*args, **kwargs)
