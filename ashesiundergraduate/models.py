from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from setup.models import Application

class PersonalInformation(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    BOOL_CHOICES = (
        (True, 'Yes'),
        (False, 'No'),
    )

    application = models.OneToOneField(Application)
    middle_name = models.CharField(_('middle name'), max_length=30)
    date_of_birth = models.DateField(_('date of birth'), null=True)
    applied_before = models.NullBooleanField(_('applied before'), choices=BOOL_CHOICES)
    year_applied = models.CharField(_('year applied'), max_length=4, null=True)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, null=True)
    # photo = 

    def __str__(self):
        return '%s %s %s' % (self.user.first_name, self.middle_name, self.user.last_name)
