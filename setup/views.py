from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Application

class ApplicationList(ListView):
    model = Application
    context_object_name = 'applications'

class ApplicationDetail(DetailView):
    model = Application
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetail, self).get_context_data(**kwargs)
        context['application_completion'] = 0.5
        return context

def application_form(request, orgname, slug, form_slug):
    print orgname, slug, form_slug

    return render(request, 'setup/application_form_detail.html', {})
