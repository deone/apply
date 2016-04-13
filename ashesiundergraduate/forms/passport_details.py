from django import forms
from django.conf import settings

from utils.getters import get_obj_from_form

from ..models import PassportCheck, PassportDetails

class PassportCheckForm(forms.ModelForm):

    class Meta:
        model = PassportCheck
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user_application = get_obj_from_form(kwargs)
        super(PassportCheckForm, self).__init__(*args, **kwargs)

    def save(self):
        data = self.cleaned_data
        passport_check, created = PassportCheck.get_or_create(user_application=self.user_application, defaults=data)
        if not created:
            passport_check.have_passport = data['have_passport']
            passport_check.save()

        return passport_check

class BasePassportDetailsFormSet(forms.BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        self.passport_check = get_obj_from_form(kwargs)
        super(BasePassportDetailsFormSet, self).__init__(*args, **kwargs)
        self.forms[0].empty_permitted = False

    def add_fields(self, form, index):
        super(BasePassportDetailsFormSet, self).add_fields(form, index)
        form.fields['expiry_date'] = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control date'}))
        form.fields['expiry_date'].input_formats = settings.DATE_INPUT_FORMATS

    def save(self):
        instances = super(BasePassportDetailsFormSet, self).save(commit=False)
        for instance in instances:
            instance.passport_check = self.passport_check
            instance.save()
        return instances

PassportDetailsFormSet = forms.modelformset_factory(PassportDetails,
    exclude=('passport_check',),
    widgets={
      'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
      'expiry_date': forms.TextInput(attrs={'class': 'form-control date'}),
      },
    formset=BasePassportDetailsFormSet, extra=2, max_num=2)
