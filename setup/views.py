from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .models import Application
from utils.getters import get_application, get_user_application, compute_completion, get_registry_key
from utils.registry import REGISTRY


def unslugify(slug):
    unslug = ''
    parts = slug.split('-')
    for part in parts:
        unslug += part.title() + ' '

    return unslug[:-1]

def get_context_variables(userapp, application):

    return {
        'application_completion': compute_completion(userapp.form_filled_count, application.applicationform_set.count()),
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
    """ registry_key = orgname + slug.split('-')[0]
    application = get_application(slug)

    form_class =  REGISTRY[registry_key][form_slug]

    if request.method == "POST":
        print request.POST
        form = form_class(request.POST, user=request.user, application=application)
        if form.is_valid():
            form.save()
        else:
            print form.errors
            return redirect('application_form', orgname=orgname, slug=slug, form_slug=form_slug)
    else:
        form = form_class(user=request.user, application=application)

    userapp = get_user_application(request.user, application)
    template_name = '%s%s%s%s' % (registry_key, '/', form_slug, '.html')

    context = get_context_variables(userapp, application)
    context.update({
      'form_name': unslugify(form_slug),
      'form': form,
      })

    return render(request, template_name, context) """

    registry_key = orgname + slug.split('-')[0]
    form_class =  REGISTRY[registry_key][form_slug]
    application = get_application(slug)
    userapp = get_user_application(request.user, application)

    if request.method == "POST":
        form = form_class(request.POST, user=request.user, application=application)
        if form.is_valid():
            form.save()
    else:
        form = form_class(user=request.user, application=application)

    template_name = '%s%s%s%s' % (registry_key, '/', form_slug, '.html')

    context = get_context_variables(userapp, application)
    context.update({
      'form_name': unslugify(form_slug),
      'form': form,
      })

    return render(request, template_name, context)
