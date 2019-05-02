import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from person_app.models import Person, Birth
from core.models import (
    DateTime,
    GivName,
    SurName,
    SURNAME_DICT,
)

pytestmark = pytest.mark.django_db


class TestBirth:
    def test_birth(self):
        instance = mixer.blend(Birth)
        assert instance
        assert instance.pk

    def test_person(self):
        person = mixer.blend(Person)
        birth = mixer.blend(Birth)
        birth.person = person.pk
        birth.save()
        assert birth.person == person

        person = mixer.blend(Person)
        birth.person = person
        birth.save()
        assert birth.person == person

    def test_givname_getter(self):
        birth = mixer.blend(Birth)

        assert not birth.givname

        birth._givname = GivName.objects.create(givname='abc')
        birth.save()
        assert birth.givname == 'abc'

    def test_givname_setter(self):
        birth = mixer.blend(Birth)

        assert birth._givname is None

        # Argument is str
        birth.givname = 'Yyyий'
        birth.save()
        assert birth._givname.givname == 'Yyyий'
        birth.givname = None
        birth.save()
        assert birth._givname is None

        # Argument is GivName
        birth.givname = GivName.objects.create(givname='Yyyий')
        birth.save()
        assert birth._givname.givname == 'Yyyий'
        birth.givname = None
        birth.save()
        assert birth._givname is None

    def test_surname_getter(self):
        birth = mixer.blend(Birth)

        assert birth.surname == ''

        # Male
        birth.gender = 'M'
        birth._surname = SurName.objects.create(
            _surname_male='Yyyий',
            _surname_female='Xxxая',
        )
        birth.save()
        assert birth.surname == 'Yyyий'

        # Female
        birth.gender = 'F'
        birth.save()
        assert birth.surname == 'Xxxая'

    def test_surname_setter(self):
        birth = mixer.blend(Birth)

        assert birth._surname is None

        # Male
        birth.gender = 'M'

        # Argument is str
        birth.surname = 'Yyyий'
        birth.save()
        assert birth._surname._surname_male == 'Yyyий'
        birth.surname = None
        birth.save()
        assert birth._surname is None

        # Argument is SurName
        birth.surname = SurName.objects.create(_surname_male='Yyyий')
        birth.save()
        assert birth._surname._surname_male == 'Yyyий'
        birth.surname = None
        birth.save()
        assert birth._surname is None

        # Female
        birth.gender = 'F'

        # Argument is str
        birth.surname = 'Xxxая'
        birth.save()
        assert birth._surname._surname_female == 'Xxxая'
        birth.surname = None
        birth.save()
        assert birth._surname is None

        # Argument is SurName
        birth.surname = SurName.objects.create(_surname_female='Xxxая')
        birth.save()
        assert birth._surname._surname_female == 'Xxxая'
        birth.surname = None
        birth.save()
        assert birth._surname is None

    dt_data = {
        'year': 2000,
        'month': 6,
        'day': 15,
        'hour': 12,
        'minute': 30,
    }

    def test_datetime_getter(self):
        birth = mixer.blend(Birth)

        assert not birth._datetime

        obj = mixer.blend(DateTime)
        for key in self.dt_data:
            value = self.dt_data.get(key)
            setattr(obj, key, value)
        obj.save()
        birth._datetime = obj
        assert birth.datetime == self.dt_data

    def test_datetime_setter(self):
        birth = mixer.blend(Birth)

        assert birth._datetime is None

        birth.datetime = self.dt_data
        birth.save()
        for key in self.dt_data:
            value = self.dt_data.get(key)
            assert getattr(birth._datetime, key, value) == value

        birth.datetime = None
        birth.save()
        assert birth._datetime is None

    def test_link(self):
        data = {
            'givname': [GivName, 'Иван', '_givname'],
            'surname': [SurName, 'Иванов', '_surname'],
            'datetime': [DateTime, self.dt_data, '_datetime'],
            #'datetime': [DateTime, {}, '_datetime'],
        }

        for key in data:
            obj = data.get(key)[0]
            value = data.get(key)[1]
            _ = data.get(key)[2]

            birth = mixer.blend(Birth)
            bpk1 = birth.pk
            setattr(birth, key, value)
            birth.save()
            assert obj.objects.all().count() == 1
            assert obj.objects.filter(link=1).count() == 1

            birth = mixer.blend(Birth)
            bpk2 = birth.pk
            setattr(birth, key, value)
            birth.save()
            assert obj.objects.all().count() == 1
            assert obj.objects.filter(link=2).count() == 1

            birth = Birth.objects.get(pk=bpk1)
            setattr(birth, key, None)
            birth.save()
            assert obj.objects.all().count() == 1
            assert obj.objects.filter(link=1).count() == 1

            Birth.objects.get(pk=bpk2).delete()
            assert obj.objects.all().count() == 0

            if hasattr(obj, 'note'):
                instance = mixer.blend(obj)
                instance.note = 'Hello'
                instance.save()
                birth = Birth.objects.get(pk=bpk1)
                setattr(birth, key, value)
                birth.save()
                assert obj.objects.get(link=1)

                birth = mixer.blend(Birth)
                bpk2 = birth.pk
                birth = Birth.objects.get(pk=bpk2)
                setattr(birth, key, value)
                birth.save()
                assert obj.objects.get(link=2)

                Birth.objects.get(pk=bpk2).delete()
                assert obj.objects.get(link=1)

                birth = Birth.objects.get(pk=bpk1)
                setattr(birth, key, None)
                birth.save()
                assert obj.objects.get(link=0)
                assert obj.objects.all().count() == 1
                o = obj.objects.get(link=0)
                o.note = ''
                o.save()

            obj.objects.all().delete()

    def test_likes(self):
        user1 = mixer.blend(get_user_model())
        user2 = mixer.blend(get_user_model())
        obj = Birth.objects.create(
            person=mixer.blend(Person),
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
        birth1 = Birth.objects.create(
            givname="Иван",
            surname="Иванов"
        )
        assert Person.objects.all().count() == 1

        person = Person.objects.get(pk=birth1.pk)
        birth2 = Birth.objects.create(
            person=person,
            givname="Иван",
            surname="Иванов"
        )
        assert Person.objects.all().count() == 1

    def test_delete(self):
        birth = Birth.objects.create()
        assert birth._person is not None
        person = mixer.blend(Person)
        assert Person.objects.all().count() == 2
        birth._person = person
        birth.save()
        assert Person.objects.all().count() == 2
        Birth.objects.create()
        assert Person.objects.all().count() == 3
