from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver

from registration.signals import user_registered


@receiver(user_registered)
def user_created(sender, user, request, **kwargs):
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.save()
