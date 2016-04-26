from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from setup.models import Application

@login_required
def index(request, orgname):
    return render(request, 'staffadmin/index.html', {})

@login_required
def user_application_list(request, orgname, pk):
    application = get_object_or_404(Application, pk=pk)
    return render(request, 'staffadmin/user_application_list.html', {'application': application})
