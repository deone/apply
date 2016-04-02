from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Application

class ApplicationListView(ListView):
    model = Application
    context_object_name = 'applications'

class ApplicationDetailView(DetailView):
    model = Application
    context_object_name = 'application'
