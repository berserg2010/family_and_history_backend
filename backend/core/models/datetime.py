from django.db import models
from django.forms import model_to_dict

from . import choices


class DateTime(models.Model):
    year = models.PositiveSmallIntegerField(
        default=None,
        blank=True,
        null=True,
    )
    month = models.PositiveSmallIntegerField(
        default=None,
        blank=True,
        null=True,
    )
    day = models.PositiveSmallIntegerField(
        default=None,
        blank=True,
        null=True,
    )
    hour = models.PositiveSmallIntegerField(
        default=None,
        blank=True,
        null=True,
    )
    minute = models.PositiveSmallIntegerField(
        default=None,
        blank=True,
        null=True,
    )
    qualifiers = models.CharField(
        max_length=4,
        choices=choices.QUALIFIERS_CHOICES,
        default='EXC',
    )
    calendar = models.CharField(
        max_length=9,
        choices=choices.CALENDAR_CHOICES,
        default='Gregorian',
    )
    link = models.PositiveSmallIntegerField(
        default=0,
    )

    # unique_together = ((
    #                        'year',
    #                        'month',
    #                        'day',
    #                        'hour',
    #                        'minute',
    #                        'qualifiers',
    #                        'calendar',
    #                    ),)

    # between = models.OneToOneField(
    #     'DateTime',
    #     on_delete=models.CASCADE,
    #     related_name='datetime_between',
    #     blank=True,
    #     null=True,
    #     default=None,
    # )

    @property
    def datetime(self):
        return model_to_dict(
            DateTime.objects.get(pk=self.pk),
            ['year', 'month', 'day', 'hour', 'minute'],
        )

    @datetime.setter
    def datetime(self, kwargs):
        check_is_data = None

        if kwargs:
            kwargs.update({key: None for key, value in kwargs.items() if value == ''})
            check_is_data = tuple(value for key, value in kwargs.items() if value is not None)

        if check_is_data:
            self.year = kwargs.get('year')
            self.month = kwargs.get('month')
            self.day = kwargs.get('day')
            self.hour = kwargs.get('hour')
            self.minute = kwargs.get('minute')

            # if self.pk:
            #     # datetime = DateTime.objects.get(pk=self.pk)
            #     self.objects.update(
            #         day=value.get('day'),
            #         month=value.get('month'),
            #         year=value.get('year'),
            #         hour=value.get('hour'),
            #         minute=value.get('minute'),
            #     )
            # else:
            #     DateTime.objects.create(
            #         day=value.get('day'),
            #         month=value.get('month'),
            #         year=value.get('year'),
            #         hour=value.get('hour'),
            #         minute=value.get('minute'),
            #     )
        # elif instance_pk:
        #     DateTime.objects.get(pk=instance_pk).delete()
    #
    # def __str__(self):
    #     if self.year and self.month and self.day:
    #         return '%s' % (date(self.year, self.month, self.day).strftime('%d %b %Y'))
    #     # year = month = day = None
    #
    #     if self.year is None:
    #         year = '----'
    #     else:
    #         year = self.year
    #
    #     if self.month is None:
    #         month = '--'
    #     else:
    #         month = self.month
    #
    #     if self.day is None:
    #         day = '--'
    #     else:
    #         day = self.day
    #
    #     return '%s %s %s' % (day, month, year)
