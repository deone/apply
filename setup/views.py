from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.apps import apps

from utils.getters import *
from utils.registry import REGISTRY

from .models import Application, SavedForm

def get_initial_data(registry_key, model_name, form_type, user_app, attr):
    model = apps.get_model(registry_key, model_name)
    if form_type == 'form':
        try:
            obj = model.objects.get(user_application=user_app)
        except model.DoesNotExist:
            obj = data = None
        else:
            data = obj.to_dict()
    else:
        data = None

    if attr is not None and obj is not None:
        try:
            dep_data = getattr(obj, attr).to_dict()
        except:
            # we need to catch RelatedObjectDoesNotExist here
            dep_data = None
    else:
        dep_data = None

    return data, dep_data

def process_forms(request, form_dict, data, dep_data, **kwargs):
    dep_form_dict = form_dict.get('dependence', None)
    if dep_form_dict is not None:
        dep_form_class = dep_form_dict['class']
    else:
        dep_form_class = dep_form = None

    main_form = form_dict['class'](request.POST, request.FILES, initial=data, **kwargs)
    if main_form.is_valid():
        obj = main_form.save()

        if dep_form_class is not None:
            dep_form = dep_form_class(request.POST, request.FILES, initial=dep_data, obj=obj)
            if dep_form.is_valid():
                obj = dep_form.save()
                return main_form, dep_form, True
        else:
            return main_form, None, True

    return main_form, dep_form, False

class ApplicationList(ListView):
    model = Application
    context_object_name = 'applications'

def application_index(request, orgname, slug):
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
    # Get registry key
    registry_key = orgname + slug.split('-')[0]

    # Get form registry entry
    form_dict = REGISTRY[registry_key][form_slug]
    form_class, form_type = get_form_class_and_type(form_dict)
    if 'dependence' in form_dict:
        dependence_class, dependence_type = get_form_class_and_type(form_dict['dependence'])
    else:
        dependence_class = dependence_type = dep_form = None

    application = get_application(slug)
    user_app = get_user_application(request.user, application)

    saved_forms = [sf.form_slug for sf in user_app.savedform_set.all()]
    form_name = unslugify(form_slug)

    template_name = '%s%s%s%s' % (registry_key, '/', form_slug, '.html')
    context = get_context_variables(user_app, application)

    # Get initial data
    model_name = ''.join(form_name.split(' '))
    dep = form_dict.get('dependence', None)
    if dep is not None:
        attr = dep.get('attr', None)
    else:
        attr = None
    data, dep_data = get_initial_data(registry_key, model_name, form_type, user_app, attr)
 
    ##############################################

    ################## Soul ######################
    if request.method == "POST":
        main_form, dep_form, saved = process_forms(request, form_dict, data, dep_data, obj=user_app)
        if saved:
            if form_slug not in saved_forms:
                SavedForm.objects.create(user_application=user_app, form_slug=form_slug)
            messages.success(request, '%s saved.' % form_name)
            return redirect('application_form', orgname=orgname,
                slug=slug, form_slug=get_next_form_slug(application, form_slug))
    else:
        main_form = form_class(obj=user_app, initial=data)
        if dependence_class:
            dep_form = dependence_class(obj=None, initial=dep_data)
    ###############################################

    ################## Template ###################
    # Context contains application, user_application and application_completion
    context.update({
      'form_name': form_name,
      'form': main_form,
      'dep_form': dep_form,
      'saved_forms': saved_forms,
      })

    return render(request, template_name, context)
