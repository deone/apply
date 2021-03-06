from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.sites.models import Site
from django.utils import timezone

from utils.getters import *
from utils.registry import REGISTRY

from .models import Application, SavedForm, Organization
from payments.models import Payment

def process_forms(request, form_dict, data, dep_data, **kwargs):
    dep_form_dict = form_dict.get('dependence', None)
    if dep_form_dict is not None:
        dep_form_class = dep_form_dict['class']
    else:
        dep_form_class = dep_form = None

    main_form = form_dict['class'](request.POST, request.FILES, initial=data, **kwargs)
    if main_form.is_valid():
        obj = main_form.save(commit=False)

        if dep_form_class is not None:
            dep_form = dep_form_class(request.POST, request.FILES, initial=dep_data, obj=obj)
            try:
                boolean = dep_form.is_valid()
            except AttributeError:
                # this is thrown if form is not bound because the main form determining field is not set to the required value.
                main_form.save()
                return main_form, dep_form, True
            else:
                # we can continue validating here since AttributeError is not raised.
                # main form determining field is set to the required value.
                if boolean is True:
                    obj = main_form.save()
                    dep_form.save(obj)
                    return main_form, dep_form, True
        else:
            main_form.save()
            return main_form, None, True

    return main_form, dep_form, False

def applicant_home(request):
    # Redirect staff if they ever land here after logging in.
    try:
        staff = request.user.staff
    except:
        staff = None
    else:
        return redirect('staffadmin:home', orgname=staff.organization.slug)

    if request.user.is_authenticated():
        return render(request, 'setup/application_list.html', {
          'applications': Application.objects.all(),
          })
    else:
        return render(request, 'home.html', {})

class OrganizationDetail(DetailView):
    model = Organization
    context_object_name = 'organization'

@login_required
def application_index(request, orgname, slug):
    """
    We tried to use a data migration to set the site name and domain
    for different sites e.g. dev site should have 'Apply Central Dev'
    as name and 'localhost:8000' as domain.

    We would have to load the data here because we would need it to
    set the return_url for payments. At least till we figure out how
    perform the data migration.
    """
    current_site = Site.objects.get_current()
    if current_site.name == 'example.com':
        pk = current_site.pk
        if pk == 1:
            current_site.name = 'Apply Central Dev'
            current_site.domain = 'localhost:8000'
        elif pk == 2:
            current_site.name = 'Apply Central Demo'
            current_site.domain = 'demo.applycentral.net'
        elif pk == 3:
            current_site.name = 'Apply Central'
            current_site.domain = 'applycentral.net'
        current_site.save()

    registry_key, application, user_app, context = get_form_variables(request.user, orgname, slug)

    ##################### Submit Application ############################
    # Insert payment and update user application
    if user_app.application.has_fee:
        paid = getattr(user_app, 'payment', None)
        payment_token = request.GET.get('token', None)
        if paid is None and payment_token is not None:
            Payment.objects.create(user_application=user_app, token=payment_token)
            return redirect('success', orgname=orgname, slug=slug)
    ######################################################################

    template_name = '%s%s%s' % (registry_key, '/', 'index.html')

    return render(request, template_name, context)

@login_required
def application_form(request, orgname, slug, form_slug):
    ################## Variables #################
    registry_key, application, user_app, context = get_form_variables(request.user, orgname, slug)

    # Get form registry entry
    form_dict = REGISTRY[registry_key][form_slug]
    form_class, form_type = get_form_class_and_type(form_dict)
    if 'dependence' in form_dict:
        dependence_class, dependence_type = get_form_class_and_type(form_dict['dependence'])
    else:
        dependence_class = dependence_type = dep_form = None

    form_name = unslugify(form_slug)

    template_name = '%s%s%s%s' % (registry_key, '/', form_slug, '.html')

    # Get initial data
    model_name = form_class.__name__[:-4]
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
            if form_slug not in context['saved_forms']:
                SavedForm.objects.create(user_application=user_app, form_slug=form_slug)
            messages.success(request, '%s saved.' % form_name)
            return redirect('application_form', orgname=orgname,
                slug=slug, form_slug=get_next_form_slug(application, form_slug))
    else:
        main_form = form_class(obj=user_app, initial=data)
        if dependence_class:
            if dependence_type == 'formset':
                kwarg = {}
                dep_model = apps.get_model(registry_key, attr)
                queryset_key = dep.get('queryset_key', None)
                if queryset_key is not None:
                    kwarg[queryset_key] = user_app
                dep_form = dependence_class(obj=None, initial=dep_data, queryset=dep_model.objects.filter(**kwarg))
            else:
                dep_form = dependence_class(obj=None, initial=dep_data)
    ###############################################

    ################## Template ###################
    # Context contains application, user_application and application_completion
    completion = context['application_completion']
    context.update({
      'form_name': form_name,
      'form': main_form,
      'dep_form': dep_form,
      'feedback': get_feedback(completion),
      })

    return render(request, template_name, context)

def get_feedback(completion):
    c = round(completion, 1)
    if c == 0.0:
        return "Start"
    if c == 0.1:
        return 'Good job!'
    if c == 0.2:
        return 'Awesome!'
    if c == 0.3:
        return 'Keep going!'
    if c == 0.4:
        return 'Great job!'
    if c == 0.5:
        return "Hurray! You're halfway"
    if c == 0.6:
        return "Keep it up!"
    if c == 0.7:
        return "Cross your t's"
    if c == 0.8:
        return "Dot your i's"
    if c == 0.9:
        return 'Almost done...'
    if c == 1.0:
        return 'Review form before submitting'

@login_required
def success(request, orgname, slug):
    registry_key, application, user_app, context = get_form_variables(request.user, orgname, slug)

    if not user_app.is_complete:
        user_app.is_complete = True
        user_app.submit_date = timezone.now()
        user_app.save()

    template = '%s%s%s' % (registry_key, '/', 'success.html')

    context.update({
      'feedback': get_feedback(context['application_completion']),
    })

    return render(request, template, context)
