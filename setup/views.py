from django.shortcuts import render
from django.views.generic import ListView

from .models import Application

class ApplicationListView(ListView):
    model = Application
    context_object_name = 'applications'
