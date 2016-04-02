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
    name = models.CharField(_('application name'), max_length=50)
    slug = AutoSlugField(populate_from='name', db_index=False, editable=False)
    is_open = models.BooleanField(_('is open'), default=False)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.name

class Staff(models.Model):
    user = models.OneToOneField(User)
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return self.user.get_full_name()

class Form(models.Model):
    application = models.ForeignKey(Application)
    name = models.CharField(_('form name'), max_length=50)

    def __str__(self):
        return '%s %s' % (self.application.name, self.name)
