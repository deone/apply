from django import forms

from utils.getters import get_user_app_from_form

from ..models import PassportDetails

class BasePassportDetailsFormSet(forms.BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        self.user_application = get_user_app_from_form(kwargs)
        super(BasePassportDetailsFormSet, self).__init__(*args, **kwargs)

    def add_fields(self, form, index):
        super(BasePassportDetailsFormSet, self).add_fields(form, index)
        form.fields['expiry_date'] = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control date'}))

PassportDetailsFormSet = forms.modelformset_factory(PassportDetails,
    exclude=(),
    widgets={
      'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
      'expiry_date': forms.TextInput(attrs={'class': 'form-control date'}),
      },
    formset=BasePassportDetailsFormSet, extra=2, max_num=2)

""" class PassportDetailsForm(forms.ModelForm):

    class Meta:
        model = PassportDetails
        exclude = ['user_application']

    def __init__(self, *args, **kwargs):
        self.user_application = get_user_app_from_form(kwargs)
        super(PassportDetailsForm, self).__init__(*args, **kwargs)
        self.fields['passport_number'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['expiry_date'].widget = forms.TextInput(attrs={'class': 'form-control date'})
        self.fields['expiry_date'].input_formats = settings.DATE_INPUT_FORMATS

    def save(self):
        data = self.cleaned_data
        passport_details, created = PassportDetails.objects.get_or_create(user_application=self.user_application, defaults=data)
        if not created:
            passport_details.passport_number = data['passport_number']
            passport_details.expiry_date = data['expiry_date']

        return passport_details """
