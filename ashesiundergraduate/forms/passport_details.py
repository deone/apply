from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from utils.getters import get_obj_from_form

from ..models import PassportCheck, PassportDetails, BOOL_CHOICES

class PassportCheckForm(forms.ModelForm):

    class Meta:
        model = PassportCheck
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user_application = get_obj_from_form(kwargs)
        super(PassportCheckForm, self).__init__(*args, **kwargs)
        self.fields['have_passport'].label = _('Do you have a passport?')
        self.fields['have_passport'].widget = forms.RadioSelect(choices=BOOL_CHOICES)

    def save(self, commit=True):
        if commit is False:
            return super(PassportCheckForm, self).save(commit=False)
        else:
            data = self.cleaned_data
            passport_check, created = PassportCheck.objects.get_or_create(user_application=self.user_application, defaults=data)
            if not created:
                passport_check.have_passport = data['have_passport']
                passport_check.save()

            return passport_check

class BasePassportDetailsFormSet(forms.BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        self.passport_check = get_obj_from_form(kwargs)
        if self.passport_check is not None:
            if not self.passport_check.have_passport:
                return
        super(BasePassportDetailsFormSet, self).__init__(*args, **kwargs)
        self.forms[0].empty_permitted = False

    def add_fields(self, form, index):
        super(BasePassportDetailsFormSet, self).add_fields(form, index)
        form.fields['expiry_date'] = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control date'}))
        form.fields['expiry_date'].input_formats = settings.DATE_INPUT_FORMATS

    def save(self, passport_check):
        instances = super(BasePassportDetailsFormSet, self).save(commit=False)
        for instance in instances:
            instance.passport_check = passport_check
            instance.save()
        return instances

PassportDetailsFormSet = forms.modelformset_factory(PassportDetails,
    exclude=('passport_check',),
    widgets={
      'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
      'expiry_date': forms.TextInput(attrs={'class': 'form-control date'}),
      },
    formset=BasePassportDetailsFormSet, extra=2, max_num=2)
