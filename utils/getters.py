from django.shortcuts import get_object_or_404

from setup.models import Application, UserApplication

def get_user_app_from_form(dct):
    return dct.pop('user_application', None)

def get_application(slug):
    return get_object_or_404(Application, slug=slug)

def get_user_application(user, application):
    user_app, created = UserApplication.objects.get_or_create(user=user, application=application)
    return user_app

def compute_completion(form_filled_count, application_form_count):
    return form_filled_count / float(application_form_count)

def get_registry_key(org_name, application_slug):
    return '%s%s' % (org_name, application_slug.split('-')[0])

def get_next_form_slug(application, current_slug):
    form_slugs = [af.slug for af in application.applicationform_set.all()]
    if form_slugs.index(current_slug) != len(form_slugs) - 1:
        next_form_slug = form_slugs[form_slugs.index(current_slug) + 1]
    else:
        next_form_slug = current_slug

    return next_form_slug
