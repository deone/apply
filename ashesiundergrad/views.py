from django.shortcuts import render, get_object_or_404

from setup.models import Application

def get_application(slug):
    return get_object_or_404(Application, slug=slug)

def index(request, orgname, slug):

    return render(request, 'ashesiundergrad/index.html',
        {
          'application_completion': 1,
          'application': get_application(slug),
        })
