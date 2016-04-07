from ashesiundergraduate.forms import *

REGISTRY = {
      'ashesiundergraduate': {
        'personal-information': {'form': PersonalInformationForm},
        'citizenship': {'form': CitizenshipForm},
        'passport-details': {'form': PassportDetailsForm, 'count': 2},
        'scholarships': {'form': ScholarshipsForm},
      },
    }
