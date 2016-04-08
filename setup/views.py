from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django import forms
from django.apps import apps

from utils.getters import *
from utils.registry import REGISTRY

from .models import Application, SavedForm

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
    ################## Variables #################
    registry_key = orgname + slug.split('-')[0]
    form_class = REGISTRY[registry_key][form_slug]

    application = get_application(slug)
    user_app = get_user_application(request.user, application)

    saved_forms = [sf.form_slug for sf in user_app.savedform_set.all()]
    form_name = unslugify(form_slug)

    template_name = '%s%s%s%s' % (registry_key, '/', form_slug, '.html')
    context = get_context_variables(user_app, application)

    model = apps.get_model(registry_key, ''.join(form_name.split(' ')))

    if not issubclass(form_class, forms.BaseModelFormSet):
        try:
            obj = model.objects.get(user_application=user_app)
        except model.DoesNotExist:
            data = None
        else:
            data = obj.to_dict()
    ##############################################

    ################## Soul ######################
    if request.method == "POST":
        if issubclass(form_class, forms.BaseModelFormSet):
            form = form_class(request.POST, request.FILES)
        else:
            form = form_class(request.POST, request.FILES, user_application=user_app, initial=data)

        if form.is_valid():
            if issubclass(form_class, forms.BaseModelFormSet):
                instances = form.save(commit=False)
                for instance in instances:
                    instance.user_application = user_app
                    instance.save()
            else:
                form.save()

            if form_slug not in saved_forms:
                SavedForm.objects.create(user_application=user_app, form_slug=form_slug)
            messages.success(request, '%s saved.' % form_name)
            return redirect('application_form', orgname=orgname,
                slug=slug, form_slug=get_next_form_slug(application, form_slug))
    else:
        if issubclass(form_class, forms.BaseModelFormSet):
            form = form_class()
        else:
            form = form_class(user_application=user_app, initial=data)
    ###############################################

    ################## Template ###################
    # Context contains application, user_application and application_completion
    context.update({
      'form_name': form_name,
      'form': form,
      'saved_forms': saved_forms,
      })

    return render(request, template_name, context)
