from django import forms

from utils.getters import get_user_app_from_form

from ..models import Scholarships

class ScholarshipsForm(forms.ModelForm):

    class Meta:
        model = Scholarships
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user_application = get_user_app_from_form(kwargs)
        super(ScholarshipsForm, self).__init__(*args, **kwargs)
