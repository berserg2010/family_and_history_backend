from django.db import models

from core.models import (
    choices,
    ObjectField,
)
from person_app.models import Birth


class Family(ObjectField):
    child = models.ManyToManyField(
        Birth,
        through='Child',
    )


class Child(models.Model):
    _family = models.ForeignKey(
        Family,
        related_name='%(class)s_family_set',
        related_query_name='%(class)ss_family',
        null=False,
        on_delete=models.CASCADE,
    )
    _birth = models.ForeignKey(
        Birth,
        related_name='%(class)s_birth_set',
        related_query_name='%(class)ss_birth',
        null=False,
        on_delete=models.CASCADE,
    )
    reltofath = models.CharField(
        max_length=1,
        choices=choices.REL_CHOICES,
        default='B',
    )
    reltomoth = models.CharField(
        max_length=1,
        choices=choices.REL_CHOICES,
        default='B',
    )
    childnbrfath = models.PositiveSmallIntegerField(
        default=None,
        blank=True,
        null=True,
    )
    childnbrmoth = models.PositiveSmallIntegerField(
        default=None,
        blank=True,
        null=True,
    )

    # class Meta:
    #     unique_together = ('family', 'person')

    @property
    def family(self):
        return self._family

    @family.setter
    def family(self, value):
        if isinstance(value, Family):
            self._family = value
        elif Family.objects.filter(pk=value).exists():
            self._family = Family.objects.get(pk=value)

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        if isinstance(value, Birth):
            self._birth = value
        elif Birth.objects.filter(pk=value).exists():
            self._birth = Birth.objects.get(pk=value)
