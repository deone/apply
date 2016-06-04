from django.db.models.signals import class_prepared
from django.core.validators import MaxLengthValidator
from django.conf import settings

def longer_username(sender, *args, **kwargs):
    if sender.__name__ == "User" and sender.__module__ == "django.contrib.auth.models":
        max_length = settings.USERNAME_LENGTH
        field = sender._meta.get_field("username")
        field.max_length = max_length
        field.validators.pop()
        field.validators.append(MaxLengthValidator(int(max_length)))

class_prepared.connect(longer_username)
