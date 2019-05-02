from django.db import models
from django.db.models import Q

from core.models import (
    choices,
    DateTime,
    EventField,
    GivName,
    SurName,
    link_inc,
    link_dec,
)
from person_app.person.models import Person


class Birth(EventField):
    _person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    gender = models.CharField(
        max_length=1,
        choices=choices.GENDER_CHOICES,
        default='U',
    )
    _givname = models.ForeignKey(
        GivName,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    _surname = models.ForeignKey(
        SurName,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    @property
    def person(self):
        return self._person

    @person.setter
    def person(self, value):
        if isinstance(value, Person):
            self._person = value
        elif Person.objects.filter(pk=value).exists():
            self._person = Person.objects.get(pk=value)

    @property
    def givname(self):
        if self._givname:
            return self._givname.givname
        else:
            return ''

    @givname.setter
    def givname(self, value):
        if isinstance(value, str):
            value, created = GivName.objects.get_or_create(
                givname=value,
            )

        if self._givname:
            if self._givname is not value:
                if self._givname.link > 1:
                    self._givname.link -= 1
                    self._givname.save()
                elif self._givname.note:
                    self._givname.link = 0
                    self._givname.save()
                else:
                    self._givname.delete()
            else:
                return

        link_inc(value)

        self._givname = value

    @property
    def surname(self):
        if self._surname:
            if self.gender == 'F':
                surname = self._surname.surname[1]
            else:
                surname = self._surname.surname[0]
        else:
            surname = ''
        return '%s' % surname

    @surname.setter
    def surname(self, value):
        if isinstance(value, str):
            if self.gender == 'F':
                query = SurName.objects.filter(_surname_female=value)
            else:
                query = SurName.objects.filter(_surname_male=value)

            if query.exists():
                value = (
                    SurName.objects.get(_surname_female=value)
                    if self.gender == 'F'
                    else SurName.objects.get(_surname_male=value)
                )
            else:
                value = (
                    SurName.objects.create(surname={'surname_female': value})
                    if self.gender == 'F'
                    else SurName.objects.create(surname={'surname_male': value})
                )

        if self._surname:
            if self._surname is not value:
                link_dec(self._surname)
            else:
                return

        link_inc(value)

        self._surname = value

    def save(self, *args, **kwargs):
        # if self.pk is None and self.person is None:
        if self._person is None:
            self._person = Person.objects.create()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        link_dec(self._givname)
        link_dec(self._surname)
        link_dec(self._datetime)
        super().delete(*args, **kwargs)

