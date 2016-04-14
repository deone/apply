from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone

from setup.models import UserApplication

import os

ORG_NAME = 'ashesi'
APPLICATION_NAME = 'undergraduate-application-2016'

BOOL_CHOICES = (
        (True, 'Yes'),
        (False, 'No'),
    )

def get_upload_path(instance, filename):
    now = timezone.now()
    return os.path.join('%s/%s/%s/' % (ORG_NAME, APPLICATION_NAME, now.strftime('%Y-%m-%d')), filename)

class PersonalInformation(models.Model):

    class Meta:
        verbose_name_plural = 'Personal Information'

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    ) 

    user_application = models.OneToOneField(UserApplication)
    middle_name = models.CharField(_('middle name'), max_length=30)
    date_of_birth = models.DateField(_('date of birth'))
    primary_phone_number = models.CharField(_('primary phone number'), max_length=15,
        help_text='Enter phone number in the format +233xxxxxxxxx')
    alternative_phone_number = models.CharField(_('alternative phone number'), max_length=15,
        help_text='Enter phone number in the format +233xxxxxxxxx', null=True)
    applied_before = models.NullBooleanField(_('applied before'), choices=BOOL_CHOICES)
    year_applied = models.CharField(_('year applied'), max_length=4)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to=get_upload_path,
        height_field='photo_height', width_field='photo_width',
        help_text="File name must be in the format - Firstname_Lastname.jpg")
    photo_height = models.CharField(_('photo height'), max_length=5)
    photo_width = models.CharField(_('photo width'), max_length=5)

    def to_dict(self):
        return {
            'middle_name': self.middle_name,
            'date_of_birth': self.date_of_birth.strftime(settings.DATE_INPUT_FORMATS[0]),
            'primary_phone_number': self.primary_phone_number,
            'alternative_phone_number': self.alternative_phone_number,
            'gender': self.gender,
            'applied_before': self.applied_before,
            'year_applied': self.year_applied,
            'photo': self.photo,
            }

    def __str__(self):
        return '%s %s %s' % (self.user_application.user.first_name, self.middle_name, self.user_application.user.last_name)

class Citizenship(models.Model):
    user_application = models.OneToOneField(UserApplication)
    country_of_citizenship = models.CharField(_('country of citizenship'), max_length=50)

    def __str__(self):
        return '%s %s' % (self.user_application.user.get_full_name(), self.country_of_citizenship)

    def to_dict(self):
        return {
            'country_of_citizenship': self.country_of_citizenship
        }

class PassportCheck(models.Model):
    user_application = models.ForeignKey(UserApplication)
    have_passport = models.NullBooleanField(_('have passport'), choices=BOOL_CHOICES)

    def __str__(self):
        return '%s %s' % (self.user_application.user.get_full_name(), self.have_passport)

    def to_dict(self):
        return {
            'have_passport': self.have_passport,
            }

class PassportDetails(models.Model):
    passport_check = models.ForeignKey(PassportCheck)
    passport_number = models.CharField(_('passport number'), max_length=20)
    expiry_date = models.DateField(_('expiry date'))

    class Meta:
        verbose_name_plural = _('Passport Details')

    def __str__(self):
        return self.passport_number

    def to_dict(self):
        return {
            'passport_number': self.passport_number,
            'expiry_date': self.expiry_date.strftime(settings.DATE_INPUT_FORMATS[0]),
            }

class Residence(models.Model):
    LIVING_WITH_CHOICES = (
        ('', 'Select'),
        ('PG', 'I live with my parent(s)/guardian(s)'),
        ('SELF', 'I live by myself'),
        ('ORPH', 'I live in an orphanage'),
    )

    user_application = models.OneToOneField(UserApplication)
    address = models.CharField(_('address'), max_length=255)
    town = models.CharField(_('town'), max_length=50)
    state = models.CharField(_('state'), max_length=50)
    country = models.CharField(_('country'), max_length=50)
    living_with = models.CharField(_('who do you live with?'), max_length=4, choices=LIVING_WITH_CHOICES)

    def __str__(self):
        return '%s, %s, %s' % (self.town, self.state, self.country)

    def to_dict(self):
        return {
            'address': self.address,
            'town': self.town,
            'state': self.state,
            'country': self.country,
            'living_with': self.living_with,
            }

class Orphanage(models.Model):
    residence = models.OneToOneField(Residence)
    name = models.CharField(_('name of orphanage'), max_length=50)
    contact_person_title = models.CharField(_('contact person title'), max_length=20)
    contact_person_name = models.CharField(_('contact person name'), max_length=50)
    contact_person_phone_number = models.CharField(_('contact person phone number'), max_length=15,
        help_text='Enter phone number in the format +233xxxxxxxxx')
    contact_person_email = models.EmailField(_('contact person email address'))

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'name': self.name,
            'contact_person_title': self.contact_person_title,
            'contact_person_name': self.contact_person_name,
            'contact_person_phone_number': self.contact_person_phone_number,
            'contact_person_email': self.contact_person_email,
            }

class Course(models.Model):
    name = models.CharField(_('course name'), max_length=50)

    def __str__(self):
        return self.name

class DesiredMajor(models.Model):
    user_application = models.OneToOneField(UserApplication)
    desired_major = models.ForeignKey(Course)

    def to_dict(self):
        return {
            'desired_major': self.desired_major
            }

    def __str__(self):
        return self.desired_major.name
