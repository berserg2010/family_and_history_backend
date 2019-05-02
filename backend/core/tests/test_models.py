import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
import re

from ..models import *
from person_app.models import Person, Birth


pytestmark = pytest.mark.django_db


# DateTime
class TestDateTime:
    dt_data = {
        'year': 2000,
        'month': 6,
        'day': 15,
        'hour': 12,
        'minute': 30,
    }

    def test_datetime_getter(self):
        instance = mixer.blend(DateTime)
        assert isinstance(instance, DateTime)

    def test_datetime_getter(self):
        instance = mixer.blend(DateTime)
        for key in self.dt_data:
            value = self.dt_data[key]
            setattr(instance, key, value)
        instance.save()
        assert instance.datetime == self.dt_data

    def test_datetime_setter(self):
        instance = mixer.blend(DateTime)
        for key in self.dt_data:
            assert not getattr(instance, key)

        instance.datetime = self.dt_data
        instance.save()
        for key in self.dt_data:
            value = self.dt_data[key]
            assert getattr(instance, key) == value


# Likes
class TestLikes:
    def test_likes(self):
        user1 = mixer.blend(get_user_model())
        user2 = mixer.blend(get_user_model())
        obj1 = Birth.objects.create(
            person=mixer.blend(Person),
        )

        obj1._likes.add(user1)
        assert Birth.objects.filter(_likes=user1).count() == 1
        assert obj1._likes.count() == 1

        obj1._likes.add(user2)
        assert obj1._likes.count() == 2

        obj2 = Birth.objects.create(
            person=mixer.blend(Person),
        )

        obj2._likes.add(user1)
        assert Birth.objects.filter(_likes=user1).count() == 2
        assert Person.objects.filter(birth___likes=user1).count() == 2
        assert obj2.likes == 1

        obj2._likes.remove(user1)
        assert Birth.objects.filter(_likes=user1).count() == 1
        assert Person.objects.filter(birth___likes=user1).count() == 1
        assert obj2._likes.count() == 0

        user1.person_app_birth_likes_set.add(obj2)
        assert Birth.objects.filter(_likes=user1).count() == 2
        assert Person.objects.filter(birth___likes=user1).count() == 2


# SurName
class TestSurName:
    def test_surname(self):
        instance = mixer.blend(SurName)
        assert instance

    def test_surname_getter(self):
        instance = SurName.objects.create(
            _surname_male='Yyy',
            _surname_female='Xxx',
        )
        assert instance.surname == ['Yyy', 'Xxx']

        instance._surname_female = ''
        assert instance.surname == ['Yyy', '']

    def test_surname_setter(self):
        # Male
        for key in SURNAME_DICT:
            value = SURNAME_DICT.get(key)
            instance = SurName(
                surname={'surname_male': 'Ххх{}'.format(key), },
            )
            instance.save()
            assert re.search(r'{}$'.format(key), instance._surname_male)
            assert re.search(r'{}$'.format(value), instance._surname_female)
            instance.delete()

        instance = SurName.objects.create(
            surname={'surname_male': 'Ххх'},
        )
        assert instance._surname_male == 'Ххх'
        assert instance._surname_female == 'Ххх'
        instance.delete()

        # female
        for key in SURNAME_DICT:
            value = SURNAME_DICT.get(key)
            instance = SurName(
                surname={'surname_female': 'Ххх{}'.format(value)},
            )
            instance.save()
            assert re.search(r'{}$'.format(key), instance._surname_male)
            assert re.search(r'{}$'.format(value), instance._surname_female)
            instance.delete()

        instance = SurName.objects.create(
            surname={'surname_female': 'Ххх'},
        )
        assert instance._surname_male == 'Ххх'
        assert instance._surname_female == 'Ххх'
        instance.delete()

        instance = SurName.objects.create(
            surname={
                'surname_male': 'Yyy',
                'surname_female': 'Xxx',
             },
        )
        assert instance._surname_male == 'Yyy'
        assert instance._surname_female == 'Xxx'
        instance.delete()

        instance.surname = {
            'surname_male': 'Nnn',
            'surname_female': 'Mmm',
        }
        instance.save()
        assert instance._surname_male == 'Nnn'
        assert instance._surname_female == 'Mmm'
