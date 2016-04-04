from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from utils.getters import get_application, get_user_application, compute_completion, get_registry_key
from utils.registry import REGISTRY

from .models import Application, SavedForm

def unslugify(slug):
    unslug = ''
    parts = slug.split('-')
    for part in parts:
        unslug += part.title() + ' '

    return unslug[:-1]

def get_context_variables(user_app, application):

    return {
        'application_completion': compute_completion(user_app.savedform_set.count(), application.applicationform_set.count()),
        'application': application
        }

class ApplicationList(ListView):
    model = Application
    context_object_name = 'applications'

def application(request, orgname, slug):
    application = get_application(slug)
    userapp = get_user_application(request.user, application)

    registry_key = get_registry_key(orgname, slug)
    template_name = '%s%s%s' % (registry_key, '/', 'index.html')

    return render(request, template_name, get_context_variables(userapp, application))

def application_form(request, orgname, slug, form_slug):
    registry_key = orgname + slug.split('-')[0]
    form_class =  REGISTRY[registry_key][form_slug]
    application = get_application(slug)
    user_app = get_user_application(request.user, application)

    form_slugs = [af.slug for af in application.applicationform_set.all()]
    next_form_slug = form_slugs[form_slugs.index(form_slug) + 1]

    if request.method == "POST":
        form = form_class(request.POST, user=request.user, application=application)
        if form.is_valid():
            form.save()
            SavedForm.objects.create(user_application=user_app, form_slug=form_slug)
            return redirect('application_form', orgname=orgname, slug=slug, form_slug=next_form_slug)
    else:
        form = form_class(user=request.user, application=application)

    template_name = '%s%s%s%s' % (registry_key, '/', form_slug, '.html')

    context = get_context_variables(user_app, application)
    context.update({
      'form_name': unslugify(form_slug),
      'form': form,
      'saved_forms': [sf.form_slug for sf in user_app.savedform_set.all()]
      })

    return render(request, template_name, context)
