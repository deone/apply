from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from utils import AutoSlugField

class Organization(models.Model):
    name = models.CharField(_('organization name'), max_length=50)
    short_name = models.CharField(_('organization short name'), max_length=20)

    def __str__(self):
        return self.name

class Application(models.Model):
    organization = models.ForeignKey(Organization)
    name = models.CharField(_('application name'), max_length=50)
    slug = AutoSlugField(populate_from='name', db_index=False)
    is_open = models.BooleanField(_('application open?'), default=False)
    year = models.PositiveSmallIntegerField(_('year'), null=True, blank=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return '%s %s' % (self.organization.name, self.name)

    def get_name(self):
        return '%s %s' % (self.organization.name, self.name)

    @models.permalink
    def get_absolute_url(self):
        return 'application', (self.organization.short_name.lower(), self.slug,)

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
    slug = AutoSlugField(populate_from='form.name', db_index=False, editable=False)
    form = models.ForeignKey(Form)

    def __str__(self):
        return '%s %s' % (self.application.get_name(), self.form.name)

    @models.permalink
    def get_absolute_url(self):
        return 'application_form', (self.application.organization.short_name.lower(), self.application.slug, self.slug)

class UserApplication(models.Model):
    user = models.ForeignKey(User)
    application = models.ForeignKey(Application)
    start_date = models.DateTimeField(_('start date'), default=timezone.now)
    submit_date = models.DateTimeField(_('submit date'), null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.user.get_full_name(), self.application.get_name())

class SavedForm(models.Model):
    user_application = models.ForeignKey(UserApplication)
    form_slug = models.CharField(_('form slug'), max_length=50)

    def __str__(self):
        return '%s %s' % (self.user_application.application.name, self.form_slug)
