from django import forms
from django.conf import settings

from utils.getters import get_user_app_from_form

from ..models import PassportDetails

class BasePassportDetailsFormSet(forms.BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        self.user_application = get_user_app_from_form(kwargs)
        super(BasePassportDetailsFormSet, self).__init__(*args, **kwargs)

    def add_fields(self, form, index):
        super(BasePassportDetailsFormSet, self).add_fields(form, index)
        form.fields['expiry_date'] = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control date'}))
        form.fields['expiry_date'].input_formats = settings.DATE_INPUT_FORMATS

PassportDetailsFormSet = forms.modelformset_factory(PassportDetails,
    exclude=('user_application',),
    widgets={
      'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
      'expiry_date': forms.TextInput(attrs={'class': 'form-control date'}),
      },
    formset=BasePassportDetailsFormSet, extra=2, max_num=2)
