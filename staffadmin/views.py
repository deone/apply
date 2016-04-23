from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request, orgname):
    return render(request, 'staffadmin/index.html', {})
