from django.shortcuts import get_object_or_404

from setup.models import Application, UserApplication

def get_form_variables(user, orgname, slug):
    registry_key = get_registry_key(orgname, slug)
    application = get_application(slug)
    user_app = get_user_application(user, application)
    context = get_context_variables(user_app)
    context.update({'saved_forms': [sf.form_slug for sf in user_app.savedform_set.all()]})

    return registry_key, application, user_app, context

def unslugify(slug):
    unslug = ''
    parts = slug.split('-')
    for part in parts:
        unslug += part.title() + ' '

    return unslug[:-1]

def get_form_class_and_type(dct):
    return dct['class'], dct.get('type', 'form')

def get_context_variables(user_app):

    return {
        'application_completion': compute_completion(user_app.savedform_set.count(), user_app.application.applicationform_set.count()),
        'user_application': user_app,
        }

def get_obj_from_form(dct):
    return dct.pop('obj', None)

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
