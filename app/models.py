from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class PersonalInformation(models.Model):
    user = models.OneToOneField(User)
    middle_name = models.CharField(_('middle name'), max_length=30, blank=True)
    date_of_birth = models.DateField(_('date of birth'))
    applied_before = models.BooleanField(_('applied before'))
    year_applied = models.CharField(_('year applied'), max_length=4, null=True)

    def __str__(self):
        return '%s %s %s' % (self.user.first_name, self.middle_name, self.user.last_name)

""" class Citizenship(models.Model):
    user = models.OneToOneField(User)
    country_of_citizenship = models.CharField(_('country of citizenship'), max_length=50)

class Residence(models.Model):
    LIVING_WITH_CHOICES = (
        ('', 'Select'),
        ('PG'),
        ('SELF'),
        ('ORPH'),
    )

    user = models.OneToOneField(User)
    address = models.CharField(_('address'), max_length=255)
    town = models.CharField(_('town'), max_length=50)
    state = models.CharField(_('state'), max_length=50)
    country = models.CharField(_('country'), max_length=50)
    # living_with = models.

class Major(models.Model):
    user = models.ForeignKey(User)
    # major = models.C

class Orphanage(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(_('name of orphanage'), max_length=50)
    contact_person_title = models.CharField(_('contact person title'), max_length=50)
    contact_person_name = models.CharField(_('contact person name'), max_length=50)
    contact_person_phone_number = models.CharField(_('contact person phone number'), max_length=15)
    contact_person_email = forms.EmailField(_('contact person email address'))

class Nationality(models.Model):
    user = models.ForeignKey(User)
    passport_number = models.CharField(_('passport number'), max_length=20)
    expiry_date = models.DateField(_('expiry date'))

class Course(models.Model):
    name = models.CharField(_('course name'), max_length=50) """
