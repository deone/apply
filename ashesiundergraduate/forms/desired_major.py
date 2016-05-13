from django import forms
from django.utils.translation import ugettext_lazy as _

from utils.getters import get_obj_from_form

from ..models import DesiredMajor, Course

class DesiredMajorForm(forms.ModelForm): 
    class Meta:
        model = DesiredMajor
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user_application = get_obj_from_form(kwargs)
        super(DesiredMajorForm, self).__init__(*args, **kwargs)
        self.fields['desired_major'] = forms.ModelChoiceField(Course.objects.all(),
            empty_label=_('Select'), widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        data = self.cleaned_data
        desired_major, created = DesiredMajor.objects.get_or_create(user_application=self.user_application, defaults=data)
        if not created:
            desired_major.desired_major = data['desired_major']
            desired_major.save()

        return desired_major
