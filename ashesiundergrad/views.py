from django.shortcuts import render, get_object_or_404

from setup.models import Application, UserApplication
from .forms import *

FORM_SLUG_FORM_MAP = {
    'personal-information': PersonalInformationForm
}

def get_application(slug):
    return get_object_or_404(Application, slug=slug)

def get_user_application(user, application):
    try:
        userapp = UserApplication.objects.get(user=user, application=application)
    except UserApplication.DoesNotExist:
        userapp = UserApplication.objects.create(user=user, application=application)

    return userapp

def compute_completion(form_filled_count, application_form_count):
    return form_filled_count / application_form_count

def index(request, orgname, application_slug):
    application = get_application(application_slug)
    userapp = get_user_application(request.user, application)

    return render(request, 'ashesiundergrad/index.html',
        {
          'application_completion': compute_completion(userapp.form_filled_count, application.applicationform_set.count()),
          'application': application
        })

def application_form(request, orgname, application_slug, form_slug):
    form = FORM_SLUG_FORM_MAP[form_slug]
    template = '%s%s%s' % ('ashesiundergrad/', form_slug, '.html')

    application = get_application(application_slug)
    userapp = get_user_application(request.user, application)

    return render(request, template,
        {
          'application_completion': compute_completion(userapp.form_filled_count, application.applicationform_set.count()),
          'application': application,
          'form': form
        })
