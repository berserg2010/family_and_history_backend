from django.contrib.auth import get_user_model
from django.db import models

from core.models import ObjectField


class Person(ObjectField):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
