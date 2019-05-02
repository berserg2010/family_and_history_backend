from django.db import models

from .objectfield import ObjectField


class GivName(ObjectField):
    givname = models.CharField(
        max_length=30,
        unique=True,
    )
    link = models.PositiveSmallIntegerField(
        default=0,
    )
