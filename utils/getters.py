from setup.models import Application, UserApplication
from django.shortcuts import get_object_or_404

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

def get_registry_key(org_name, application_slug):
    return '%s%s' % (org_name, application_slug.split('-')[0])
