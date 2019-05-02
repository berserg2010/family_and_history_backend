from django.db import models

from core.models import (
    EventField,
    SurName,
    link_inc,
    link_dec,
)
from person_app.models import Person
from family_app.family.models import Family


class Marriage(EventField):
    _family = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    _husband = models.ForeignKey(
        Person,
        related_name='%(class)s_husband_set',
        related_query_name='%(class)ss_husband',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    _wife = models.ForeignKey(
        Person,
        related_name='%(class)s_wife_set',
        related_query_name='%(class)ss_wife',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    _husbname = models.ForeignKey(
        SurName,
        related_name='%(class)s_husbname_set',
        related_query_name='%(class)ss_husbname',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    _wifename = models.ForeignKey(
        SurName,
        related_name='%(class)s_wifename_set',
        related_query_name='%(class)ss_wifename',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

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
    def husband(self):
        return self._husband

    @husband.setter
    def husband(self, value):
        if isinstance(value, Person):
            self._husband = value
        elif Person.objects.filter(pk=value).exists():
            self._husband = Person.objects.get(pk=value)

    @property
    def wife(self):
        return self._wife

    @wife.setter
    def wife(self, value):
        if isinstance(value, Person):
            self._wife = value
        elif Person.objects.filter(pk=value).exists():
            self._wife = Person.objects.get(pk=value)

    @property
    def husbname(self):
        if self._husbname:
            return self._husbname.surname[0]
        else:
            return ''

    @husbname.setter
    def husbname(self, value):
        if isinstance(value, str):
            query = SurName.objects.filter(_surname_male=value)

            if query.exists():
                value = SurName.objects.get(_surname_male=value)
            else:
                value = SurName.objects.create(surname={'surname_male': value})

        if self._husbname:
            if self._husbname is not value:
                link_dec(self._husbname)
            else:
                return

        link_inc(value)

        self._husbname = value

    @property
    def wifename(self):
        if self._wifename:
            return self._wifename.surname[1]
        else:
            return ''

    @wifename.setter
    def wifename(self, value):
        if isinstance(value, str):
            query = SurName.objects.filter(_surname_female=value)

            if query.exists():
                value = SurName.objects.get(_surname_female=value)
            else:
                value = SurName.objects.create(surname={'surname_male': value})

        if self._wifename:
            if self._wifename is not value:
                link_dec(self._wifename)
            else:
                return

        link_inc(value)

        self._wifename = value

    def save(self, *args, **kwargs):
        if self._family is None:
            self._family = Family.objects.create()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        link_dec(self._husbname)
        link_dec(self._wifename)
        link_dec(self._datetime)
        super().delete(*args, **kwargs)
