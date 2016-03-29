from django.shortcuts import render

from registration.backends.hmac.views import RegistrationView
from registration import signals

from .forms import ApplyRegistrationForm


class ApplyRegistrationView(RegistrationView):
    form_class = ApplyRegistrationForm

    def register(self, form):
        return super(ApplyRegistrationView, self).register(form)

    def get_success_url(self, user):
        return 'accounts:registration_complete'
