from ashesiundergraduate.forms import *

REGISTRY = {
      'ashesiundergraduate': {
        'personal-information': {'class': PersonalInformationForm},
        'citizenship': {'class': CitizenshipForm},
        'passport-details': {
          'class': PassportCheckForm,
          'dependence': {'class': PassportDetailsFormSet, 'type': 'formset', 'attr': 'passportdetails', 'queryset_key': 'passport_check__user_application'},
          },
        'residence': {
          'class': ResidenceForm,
          'dependence': {'class': OrphanageForm, 'attr': 'orphanage'},
          },
        'desired-major': {'class': DesiredMajorForm},
      },
    }
