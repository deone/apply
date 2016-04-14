from django import forms

from utils.getters import get_obj_from_form

from ..models import DesiredMajor

class DesiredMajorForm(forms.ModelForm):
    
    class Meta:
        model = DesiredMajor
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user_application = get_obj_from_form(kwargs)
        super(DesiredMajorForm, self).__init__(*args, **kwargs)
