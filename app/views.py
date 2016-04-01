from django.shortcuts import render

from app.forms import PersonalInformationForm

def index(request):
    if request.method == 'POST':
        pass
    else:
        form = PersonalInformationForm()

    return render(request, 'app/index.html', {'form': form, 'completion': .74})
