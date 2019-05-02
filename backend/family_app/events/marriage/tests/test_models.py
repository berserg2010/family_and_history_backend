import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from core.models import (
    DateTime,
    GivName,
    SurName,
)
from person_app.models import Person
from ..models import Marriage
from family_app.models import Family


pytestmark = pytest.mark.django_db


class TestMarriage:
    def test_marriage(self):
        instance = mixer.blend(Marriage)
        assert instance
        assert instance.pk

    def test_husband(self):
        person = mixer.blend(Person)
        mar = mixer.blend(Marriage)
        mar.husband = person.pk
        mar.save()
        assert mar.husband == person

        person = mixer.blend(Person)
        mar.husband = person
        mar.save()
        assert mar.husband == person

    def test_wife(self):
        person = mixer.blend(Person)
        mar = mixer.blend(Marriage)
        mar.wife = person.pk
        mar.save()
        assert mar.wife == person

        person = mixer.blend(Person)
        mar.wife = person
        mar.save()
        assert mar.wife == person

    def test_husbname_getter(self):
        marriage = mixer.blend(Marriage)

        assert marriage.husbname == ''

        marriage._husbname = SurName.objects.create(
            _surname_male='Yyyий',
            _surname_female='Xxxая',
        )
        marriage.save()
        assert marriage.husbname == 'Yyyий'

    def test_husbname_setter(self):
        marriage = mixer.blend(Marriage)

        assert marriage._husbname is None

        # Argument is str
        marriage.husbname = 'Yyyий'
        marriage.save()
        assert marriage._husbname._surname_male == 'Yyyий'
        marriage.husbname = None
        marriage.save()
        assert marriage._husbname is None

        # Argument is SurName
        marriage.husbname = SurName.objects.create(_surname_male='Yyyий')
        marriage.save()
        assert marriage._husbname._surname_male == 'Yyyий'
        marriage.husbname = None
        marriage.save()
        assert marriage._husbname is None

    def test_wifename_getter(self):
        marriage = mixer.blend(Marriage)

        assert marriage.wifename == ''

        marriage._wifename = SurName.objects.create(
            _surname_male='Yyyий',
            _surname_female='Xxxая',
        )
        marriage.save()
        assert marriage.wifename == 'Xxxая'

    def test_wifename_setter(self):
        marriage = mixer.blend(Marriage)

        assert marriage._wifename is None

        # Argument is str
        marriage.wifename = 'Xxxая'
        marriage.save()
        assert marriage._wifename._surname_female == 'Xxxая'
        marriage.wifename = None
        marriage.save()
        assert marriage._wifename is None

        # Argument is SurName
        marriage.wifename = SurName.objects.create(_surname_female='Xxxая')
        marriage.save()
        assert marriage._wifename._surname_female == 'Xxxая'
        marriage.wifename = None
        marriage.save()
        assert marriage._wifename is None

    dt_data = {
        'year': 2000,
        'month': 6,
        'day': 15,
        'hour': 12,
        'minute': 30,
    }

    def test_datetime_getter(self):
        marriage = mixer.blend(Marriage)

        assert not marriage._datetime

        obj = mixer.blend(DateTime)
        for key in self.dt_data:
            value = self.dt_data.get(key)
            setattr(obj, key, value)
        obj.save()
        marriage._datetime = obj
        assert marriage.datetime == self.dt_data

    def test_datetime_setter(self):
        marriage = mixer.blend(Marriage)

        assert marriage._datetime is None

        marriage.datetime = self.dt_data
        marriage.save()
        for key in self.dt_data:
            value = self.dt_data.get(key)
            assert getattr(marriage._datetime, key, value) == value

        marriage.datetime = None
        marriage.save()
        assert marriage._datetime is None

    def test_link(self):
        data = {
            'husbname': [SurName, 'Иванов', '_husbname'],
            'wifename': [SurName, 'Иванова', '_wifename'],
            'datetime': [DateTime, self.dt_data, '_datetime'],
            #'datetime': [DateTime, {}, '_datetime'],
        }

        for key in data:
            obj = data.get(key)[0]
            value = data.get(key)[1]
            _ = data.get(key)[2]

            marriage = mixer.blend(Marriage)
            mar1 = marriage.pk
            setattr(marriage, key, value)
            marriage.save()
            assert obj.objects.all().count() == 1
            assert obj.objects.filter(link=1).count() == 1

            marriage = mixer.blend(Marriage)
            mar2 = marriage.pk
            setattr(marriage, key, value)
            marriage.save()
            assert obj.objects.all().count() == 1
            assert obj.objects.filter(link=2).count() == 1

            marriage = Marriage.objects.get(pk=mar1)
            setattr(marriage, key, None)
            marriage.save()
            assert obj.objects.all().count() == 1
            assert obj.objects.filter(link=1).count() == 1

            Marriage.objects.get(pk=mar2).delete()
            assert obj.objects.all().count() == 0

            if hasattr(obj, 'note'):
                instance = mixer.blend(obj)
                instance.note = 'Hello'
                instance.save()
                marriage = Marriage.objects.get(pk=mar1)
                setattr(marriage, key, instance)
                marriage.save()
                assert obj.objects.get(link=1)

                marriage = mixer.blend(Marriage)
                mar2 = marriage.pk
                marriage = Marriage.objects.get(pk=mar2)
                setattr(marriage, key, instance)
                marriage.save()
                assert obj.objects.get(link=2)

                Marriage.objects.get(pk=mar2).delete()
                assert obj.objects.get(link=1)

                marriage = Marriage.objects.get(pk=mar1)
                setattr(marriage, key, None)
                marriage.save()
                assert obj.objects.get(link=0)
                assert obj.objects.all().count() == 1
                o = obj.objects.get(link=0)
                o.note = ''
                o.save()

            obj.objects.all().delete()

    def test_likes(self):
        user1 = mixer.blend(get_user_model())
        user2 = mixer.blend(get_user_model())
        obj = Marriage.objects.create(
            family=mixer.blend(Family),
        )

        obj._likes.add(user1)
        assert obj.likes == 1

        obj._likes.add(user2)
        assert obj.likes == 2

        obj._likes.remove(user1)
        assert obj.likes == 1

        obj._likes.remove(user2)
        assert obj.likes == 0

    def test_save(self):
        mar1 = Marriage.objects.create(
            husbname="Иванов",
            wifename="Иванова"
        )
        assert Family.objects.all().count() == 1

        family = Family.objects.get(pk=mar1.pk)
        mar2 = Marriage.objects.create(
            family=family,
            husbname="Иванов",
            wifename="Иванова"
        )
        assert Family.objects.all().count() == 1

    def test_delete(self):
        mar = Marriage.objects.create()
        assert mar._family is not None
        fam = mixer.blend(Family)
        assert Family.objects.all().count() == 2
        mar._family = fam
        mar.save()
        assert Family.objects.all().count() == 2
        Marriage.objects.create()
        assert Family.objects.all().count() == 3
