from django.shortcuts import render

from registration.backends.simple.views import RegistrationView

from .forms import ApplyRegistrationForm


class ApplyRegistrationView(RegistrationView):
    form_class = ApplyRegistrationForm

    def get_success_url(self, user):
        return 'app:index'
