from django.db import models

from backend.constants import DEFAULT_MAX_LENGTH

from .choices import Sex


class Person(models.Model):
    first_name = models.CharField(max_length=DEFAULT_MAX_LENGTH, null=True, blank=True)
    last_name = models.CharField(max_length=DEFAULT_MAX_LENGTH, null=True, blank=True)

    sex = models.CharField(max_length=1, choices=Sex.choices, null=True, blank=True)
