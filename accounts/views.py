from django.shortcuts import render

from registration.views import RegistrationView

from .forms import ApplyRegistrationForm


class ApplyRegistrationView(RegistrationView):
    form_class = ApplyRegistrationForm
