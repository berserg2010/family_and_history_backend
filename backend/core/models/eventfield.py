from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

from .datetime import DateTime
from .objectfield import ObjectField
from .choices import link_inc
from .choices import link_dec


class EventField(ObjectField):
    _datetime = models.ForeignKey(
        DateTime,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    _likes = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name='%(app_label)s_%(class)s_likes_set',
        related_query_name='%(app_label)s_%(class)ss_likes',
    )
    place = models.IntegerField(
        blank=True,
        null=True,
    )
    evidence = models.IntegerField(
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    @property
    def datetime(self):
        if self._datetime:
            return self._datetime.datetime
        else:
            return {}

    @datetime.setter
    def datetime(self, kwargs):
        value = None
        check_is_data = None

        if kwargs:
            kwargs.update({key: None for key, value in kwargs.items() if value == ''})
            check_is_data = tuple(value for key, value in kwargs.items() if value is not None)

        if check_is_data:
            query = DateTime.objects.filter(
                Q(year=kwargs.get('year')) &
                Q(month=kwargs.get('month')) &
                Q(day=kwargs.get('day')) &
                Q(hour=kwargs.get('hour')) &
                Q(minute=kwargs.get('minute'))
            )

            if query.exists():
                value = DateTime.objects.get(
                    Q(year=kwargs.get('year')) &
                    Q(month=kwargs.get('month')) &
                    Q(day=kwargs.get('day')) &
                    Q(hour=kwargs.get('hour')) &
                    Q(minute=kwargs.get('minute'))
                )
            else:
                value = DateTime()
                for key in kwargs:
                    val = kwargs.get(key)
                    setattr(value, key, val)
                value.save()

        if self._datetime:
            if self._datetime is not value:
                link_dec(self._datetime)
            else:
                return

        link_inc(value)

        self._datetime = value

    @property
    def likes(self):
        return self._likes.count()
