from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify

from utils import AutoSlugField

class Organization(models.Model):
    name = models.CharField(_('organization name'), max_length=50)
    slug = models.SlugField(_('slug'))

    def __str__(self):
        return self.name

class Application(models.Model):
    organization = models.ForeignKey(Organization)
    # It is important that the name field is set properly.
    # We use it to build application names and slugs and locate application form app.
    # Application form apps are named in this convention - `organization short name` + first word of application name
    # A portion of application URLs contain `organization short name` and `application slug`
    name = models.CharField(_('application name'), max_length=50)
    slug = models.SlugField(blank=True)
    year = models.PositiveSmallIntegerField(_('year'), null=True, blank=True)
    is_open = models.BooleanField(_('application open?'), default=False)
    receive_fee = models.BooleanField(_('receive fee?'), default=False)
    fee = models.PositiveSmallIntegerField(_('fee'), null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            if self.year:
                year = str(self.year)
                self.slug = slugify(self.name + ' ' + year)
                self.name += ' ' + year
            else:
                self.slug = slugify(self.name)
        super(Application, self).save(*args, **kwargs)

    def __str__(self):
        return '%s %s' % (self.organization.name, self.name)

    def get_name(self):
        return '%s %s' % (self.organization.name, self.name)

    @models.permalink
    def get_absolute_url(self):
        return 'application', (self.organization.slug.lower(), self.slug,)

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
        return 'application_form', (self.application.organization.slug.lower(), self.application.slug, self.slug)

class UserApplication(models.Model):
    user = models.ForeignKey(User)
    application = models.ForeignKey(Application)
    start_date = models.DateTimeField(_('start date'), default=timezone.now)
    submit_date = models.DateTimeField(_('submit date'), null=True, blank=True)
    is_complete = models.BooleanField(_('is complete'), default=False)

    def __str__(self):
        return '%s %s' % (self.user.get_full_name(), self.application.get_name())

class SavedForm(models.Model):
    user_application = models.ForeignKey(UserApplication)
    form_slug = models.CharField(_('form slug'), max_length=50)

    def __str__(self):
        return '%s %s' % (self.user_application.application.name, self.form_slug)
