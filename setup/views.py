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
        context['application_completion'] = 1
        return context
