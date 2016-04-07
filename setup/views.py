from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.apps import apps

from utils.getters import *
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
        'application': application,
        'user_application': user_app,
        }

class ApplicationList(ListView):
    model = Application
    context_object_name = 'applications'

def application(request, orgname, slug):
    application = get_application(slug)
    user_app = get_user_application(request.user, application)
    saved_forms = [sf.form_slug for sf in user_app.savedform_set.all()]

    registry_key = get_registry_key(orgname, slug)
    template_name = '%s%s%s' % (registry_key, '/', 'index.html')

    context = get_context_variables(user_app, application)
    context.update({'saved_forms': saved_forms})

    return render(request, template_name, context)

@login_required
def application_form(request, orgname, slug, form_slug):
    registry_key = orgname + slug.split('-')[0]
    form_class =  REGISTRY[registry_key][form_slug]

    application = get_application(slug)
    user_app = get_user_application(request.user, application)

    saved_forms = [sf.form_slug for sf in user_app.savedform_set.all()]
    form_name = unslugify(form_slug)

    model = apps.get_model(registry_key, ''.join(form_name.split(' ')))
    try:
        obj = model.objects.get(user_application=user_app)
    except model.DoesNotExist:
        obj = None

    if request.method == "POST":
        form = form_class(request.POST, request.FILES, user_application=user_app)
        if form.is_valid():
            form.save()
            if form_slug not in saved_forms:
                SavedForm.objects.create(user_application=user_app, form_slug=form_slug)
            messages.success(request, '%s saved.' % form_name)
            return redirect('application_form', orgname=orgname,
                slug=slug, form_slug=get_next_form_slug(application, form_slug))
    else:
        if obj is not None:
            data = obj.to_dict()
        else:
            data = None
        form = form_class(user_application=user_app, initial=data)

    template_name = '%s%s%s%s' % (registry_key, '/', form_slug, '.html')

    context = get_context_variables(user_app, application)
    context.update({
      'form_name': form_name,
      'form': form,
      'saved_forms': saved_forms,
      })

    return render(request, template_name, context)
