from django.shortcuts import render

def index(request, orgname, slug):
    return render(request, 'ashesiundergrad/index.html', {'application_completion': 1})
