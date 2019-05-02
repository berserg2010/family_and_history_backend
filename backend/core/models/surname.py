from django.db import models
import re

from .objectfield import ObjectField


class SurName(ObjectField):
    _surname_male = models.CharField(
        blank=True,
        max_length=30,
    )
    _surname_female = models.CharField(
        blank=True,
        max_length=30,
    )
    link = models.PositiveSmallIntegerField(
        default=0,
    )

    unique_together = (('_surname_male', '_surname_female'),)

    @property
    def surname(self):
        return [self._surname_male, self._surname_female]

    @surname.setter
    def surname(self, kwargs):
        """
        :param kwargs: surname_male, surname_female
        :return:
        """
        surname_male = kwargs.get('surname_male', '')
        surname_female = kwargs.get('surname_female', '')

        if surname_male and not surname_female:
            for key in SURNAME_DICT:
                value = SURNAME_DICT.get(key)
                if re.search(r'{}$'.format(key), surname_male):
                    self._surname_female = re.sub(r'{}$'.format(key), '{}'.format(value), surname_male)
                    self._surname_male = surname_male
                    break
            else:
                self._surname_male = self._surname_female = surname_male

        if not surname_male and surname_female:
            for key in SURNAME_DICT:
                value = SURNAME_DICT.get(key)
                if re.search(r'{}$'.format(value), surname_female):
                    self._surname_male = re.sub(r'{}$'.format(value), '{}'.format(key), surname_female)
                    self._surname_female = surname_female
                    break
            else:
                self._surname_male = self._surname_female = surname_female

        if surname_male and surname_female:
            self._surname_male = surname_male
            self._surname_female = surname_female


SURNAME_DICT = {
    'ев': 'ева',
    'ий': 'ая',
    'ин': 'ина',
    'ов': 'ова',
    # Не должно быть повторений ни в key, ни в value
    # 'ой': 'ая',
    # 'ый': 'ая',
}
