from ashesiundergraduate.forms import *

REGISTRY = {
      'ashesiundergraduate': {
        'personal-information': {'class': PersonalInformationForm},
        'citizenship': {'class': CitizenshipForm},
        'passport-details': {'class': PassportDetailsFormSet, 'type': 'formset'},
        'residence': {
          'class': ResidenceForm,
          'dependence': {'class': OrphanageForm, 'attr': 'orphanage'},
          },
        'scholarships': {'class': ScholarshipsForm},
      },
    }
