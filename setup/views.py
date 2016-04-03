from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Application
from utils.getters import get_application, get_user_application, compute_completion, get_registry_key
from utils.registry import REGISTRY


class ApplicationList(ListView):
    model = Application
    context_object_name = 'applications'

class ApplicationDetail(DetailView):
    model = Application
    context_object_name = 'application'
    template_name = 'ashesiundergraduate/application_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetail, self).get_context_data(**kwargs)
        context['application_completion'] = 0.5
        return context

def application(request, orgname, slug):
    application = get_application(slug)
    registry_key = get_registry_key(orgname, slug)
    userapp = get_user_application(request.user, application)
    template_name = '%s%s%s' % (registry_key, '/', 'index.html')

    return render(request, template_name,
        {
          'application_completion': compute_completion(userapp.form_filled_count, application.applicationform_set.count()),
          'application': application
        })

def application_form(request, orgname, slug, form_slug):
    registry_key = orgname + slug.split('-')[0]
    template_name = '%s%s%s%s' % (registry_key, '/', form_slug, '.html')

    return render(request, template_name, {})
