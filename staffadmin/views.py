from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from setup.models import Application, UserApplication

from utils.getters import get_registry_key

@login_required
def index(request, orgname):
    return render(request, 'staffadmin/index.html', {})

@login_required
def user_application(request, orgname, pk):
    user_application = get_object_or_404(UserApplication, pk=pk)
    registry_key = get_registry_key(orgname, user_application.application.slug)
    template_name = '%s%s%s' % (registry_key, '/', 'user_application.html')
    return render(request, template_name, {})

@login_required
def user_application_list(request, orgname, pk):
    application = get_object_or_404(Application, pk=pk)
    return render(request, 'staffadmin/user_application_list.html', {'application': application})
