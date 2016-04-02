from django.shortcuts import render, get_object_or_404

from setup.models import Application, UserApplication

def get_application(slug):
    return get_object_or_404(Application, slug=slug)

def compute_completion(form_filled_count, application_form_count):
    return form_filled_count / application_form_count

def index(request, orgname, application_slug):
    application = get_application(application_slug)

    try:
        userapp = UserApplication.objects.get(user=request.user, application=application)
    except UserApplication.DoesNotExist:
        userapp = UserApplication.objects.create(user=request.user, application=application)

    return render(request, 'ashesiundergrad/index.html',
        {
          'application_completion': compute_completion(userapp.form_filled_count, application.applicationform_set.count()),
          'application': application
        })

def test(request, orgname, application_slug, form_slug):
    pass
