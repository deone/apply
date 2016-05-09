# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db.models.fields import SlugField
from django.utils.translation import ugettext_lazy as _
from django import forms

class AutoSlugField(SlugField):
    """
    Auto populates itself from another field.

    It behaves like a regular SlugField.
    When populate_from is provided it'll populate itself on creation,
    only if a slug was not provided.

    P.S We don't use this anymore, but have to leave a stub because some
    migrations depend on it.
    """

    def __init__(self, *args, **kwargs):
        pass

def validate_phone_number(number):
    if not number.startswith('+'):
        raise forms.ValidationError(_('Prefix phone number with country code'), code='incorrect-number-format')

    try:
        int(number)
    except (ValueError, TypeError):
        raise forms.ValidationError(_('Enter a valid phone number'), code='invalid-phone-number')
