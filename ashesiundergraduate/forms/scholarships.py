from django import forms

from utils.getters import get_obj_from_form

from ..models import Scholarships

class ScholarshipsForm(forms.ModelForm):

    class Meta:
        model = Scholarships
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user_application = get_obj_from_form('user_application', kwargs)
        super(ScholarshipsForm, self).__init__(*args, **kwargs)
