from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from utils import AutoSlugField

class Organization(models.Model):
    name = models.CharField(_('organization name'), max_length=50)

    def __str__(self):
        return self.name

class Application(models.Model):
    organization = models.ForeignKey(Organization)
    name = models.CharField(_('application name'), max_length=50)
    slug = AutoSlugField(populate_from='name', db_index=False, editable=False)
    is_open = models.BooleanField(_('application open?'), default=False)
    deadline = models.DateTimeField()

    def __str__(self):
        return '%s %s' % (self.organization.name, self.name)

    def get_name(self):
        return '%s %s' % (self.organization.name, self.name)

class Staff(models.Model):
    user = models.OneToOneField(User)
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name_plural = _('Staff')

class Form(models.Model):
    name = models.CharField(_('form name'), max_length=50)

    def __str__(self):
        return self.name

class ApplicationForm(models.Model):
    application = models.ForeignKey(Application)
    form = models.ForeignKey(Form)

    def __str__(self):
        return '%s %s' % (self.application.get_name(), self.form.name)
