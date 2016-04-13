from django.contrib import admin

from .models import *

admin.site.register(PersonalInformation)
admin.site.register(PassportDetails)
admin.site.register(Residence)
admin.site.register(Orphanage)
