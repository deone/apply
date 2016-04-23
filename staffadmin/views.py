from django.shortcuts import render

def index(request, orgname):
    return render(request, 'staffadmin/index.html', {})
