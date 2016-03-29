from django.shortcuts import render

from registration.views import RegistrationView
from registration import signals

from .forms import ApplyRegistrationForm


class ApplyRegistrationView(RegistrationView):
    form_class = ApplyRegistrationForm

    def register(self, form):
        if form.is_valid():
            new_user = form.save()
            signals.user_registered.send(sender=self.__class__, user=new_user, request=self.request,
                first_name=self.request.POST['first_name'], last_name=self.request.POST['last_name'])
            success_url = self.get_success_url(new_user)
        return new_user

    def get_success_url(self, user):
        return 'accounts:registration_complete'
