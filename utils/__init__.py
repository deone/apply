# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

def validate_phone_number(number):
    if not number.startswith('+'):
        raise forms.ValidationError(_('Prefix phone number with country code'), code='incorrect-number-format')

    try:
        int(number)
    except (ValueError, TypeError):
        raise forms.ValidationError(_('Enter a valid phone number'), code='invalid-phone-number')
