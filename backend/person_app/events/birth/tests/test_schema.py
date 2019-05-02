import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer

from abc import ABC

from graphql_jwt.testcases import JSONWebTokenClient

from .. import schema
from person_app.models import *
from . import queries


pytestmark = pytest.mark.django_db


def test_birth_type():
    instance = schema.BirthType()
    assert instance


class BaseClass(ABC):
    def test_all_birth(self):
        mixer.blend(Birth)
        person = mixer.blend(Person)
        birth1 = mixer.blend(Birth)
        birth1.person = person
        birth1.save()
        birth2 = mixer.blend(Birth)
        birth2.person = person
        birth2.save()
        result = self.client.execute(query=queries.ALL_BIRTH)
        assert not result.errors
        assert len(result.data.get('allBirth')) == 3, 'Should return all birth'

        result = self.client.execute(query=queries.ALL_BIRTH, variables={"idPerson": person.pk})
        assert not result.errors
        assert len(result.data.get('allBirth')) == 2, 'Should return 2 births'

    def test_birth(self):
        birth = mixer.blend(Birth)
        result = self.client.execute(
            query=queries.BIRTH,
            variables={'id': birth.pk}
        )
        assert not result.errors
        assert result.data.get('birth')['id'] == str(birth.pk)

    def test_save_birth_mutation(self):
        VARIABLE = {
            "data": {
                "gender": "M",
                "givname": "Иван",
                "surname": "Иванов",
                "note": ":))",

                "year": 2000,
                "month": 6,
                "day": 15,
                "hour": 12,
                "minute": 30,
            }
        }

        if not self.user.is_authenticated:
            result = self.client.execute(
                query=queries.SAVE_BIRTH,
                variables=VARIABLE,
            )
            assert not result.errors
            assert result.data.get('saveBirth')['status'] == 403, 'Should return 403 if user is not logged in'
        else:
            result = self.client.execute(
                query=queries.SAVE_BIRTH,
                variables={"data": {
                    "gender": "",
                    "givname": "",
                    "surname": "",
                    "note": "",

                    "year": None,
                    "month": None,
                    "day": None,
                    "hour": None,
                    "minute": None,
                }},
            )
            assert not result.errors
            assert result.data.get('saveBirth')['status'] == 400

            result = self.client.execute(
                query=queries.SAVE_BIRTH,
                variables=VARIABLE,
            )
            assert not result.errors
            assert result.data.get('saveBirth')['status'] == 200, 'Should return 200 if mutation is successful'
            birth_id = int(result.data.get('saveBirth')['birth']['id'])
            assert birth_id == 1, 'Should create new birth'
            birth = Birth.objects.get(pk=birth_id)
            assert birth.gender == VARIABLE.get('data')['gender']
            assert birth.givname == VARIABLE.get('data')['givname']
            assert birth.surname == VARIABLE.get('data')['surname']
            assert birth.submitter
            assert birth.datetime == {
                "year": VARIABLE.get('data')['year'],
                "month": VARIABLE.get('data')['month'],
                "day": VARIABLE.get('data')['day'],
                "hour": VARIABLE.get('data')['hour'],
                "minute": VARIABLE.get('data')['minute'],
            }
            assert birth.note == VARIABLE.get('data')['note']

            VARIABLE = {
                "data": {
                    "id": birth_id,
                    "gender": "F",
                    "givname": "Ирина",
                    "surname": "Петрова",
                    "year": 1900,
                    "month": 12,
                    "day": 1,
                    "hour": 20,
                    "minute": 15,
                    "note": ""
                }
            }
            result = self.client.execute(
                query=queries.SAVE_BIRTH,
                variables=VARIABLE,
            )
            assert not result.errors
            assert result.data.get('saveBirth')['status'] == 200, 'Should return 200 if mutation is successful'
            birth_id = int(result.data.get('saveBirth')['birth']['id'])
            assert birth_id == 1, 'Should create new birth'
            birth = Birth.objects.get(pk=birth_id)
            assert birth.gender == VARIABLE.get('data')['gender']
            assert birth.givname == VARIABLE.get('data')['givname']
            assert birth.surname == VARIABLE.get('data')['surname']
            assert birth.submitter
            assert birth.changer
            assert birth.datetime == {
                "year": VARIABLE.get('data')['year'],
                "month": VARIABLE.get('data')['month'],
                "day": VARIABLE.get('data')['day'],
                "hour": VARIABLE.get('data')['hour'],
                "minute": VARIABLE.get('data')['minute'],
            }
            assert birth.note == VARIABLE.get('data')['note']

            person = mixer.blend(Person)

            result = self.client.execute(
                query=queries.SAVE_BIRTH,
                variables={
                    "data": {
                        "idPerson": person.pk,
                        "gender": "F",
                        "givname": "Ирина",
                        "surname": "Петрова",
                        "note": ""
                    }
                },
            )
            assert not result.errors
            assert result.data.get('saveBirth')['status'] == 200, 'Should return 200 if mutation is successful'
            birth_id = int(result.data.get('saveBirth')['birth']['id'])
            birth = Birth.objects.get(pk=birth_id)
            assert birth.person == person

    def test_delete_birth_mutation(self):
        birth = mixer.blend(Birth)

        if not self.user.is_authenticated:
            result = self.client.execute(
                query=queries.DELETE_BIRTH,
                variables={'id': birth.pk}
            )
            assert not result.errors
            assert result.data.get('deleteBirth')['status'] == 403, 'Should return 403 if user is not logged in'
        else:
            result = self.client.execute(query=queries.DELETE_BIRTH)
            assert result.errors

            result = self.client.execute(query=queries.DELETE_BIRTH, variables={'id': birth.pk})
            assert not result.errors
            assert result.data.get('deleteBirth')['status'] == 200, 'Should return 200 if mutation is successful'

    def test_search_birth(self):
        for value in ['a', 'ab', 'abc']:
            Birth.objects.create(
                person=mixer.blend(Person),
                surname=value,
            )

        result = self.client.execute(
            query=queries.SEARCH_BIRTH,
            variables={'searchTerm': 'a'}
        )
        assert not result.errors
        assert len(result.data.get('searchBirth')) == 3
        result = self.client.execute(
            query=queries.SEARCH_BIRTH,
            variables={'searchTerm': 'ab'}
        )
        assert len(result.data.get('searchBirth')) == 2
        result = self.client.execute(
            query=queries.SEARCH_BIRTH,
            variables={'searchTerm': 'abc'}
        )
        assert len(result.data.get('searchBirth')) == 1
        result = self.client.execute(
            query=queries.SEARCH_BIRTH,
            variables={'searchTerm': 'abcd'}
        )
        assert len(result.data.get('searchBirth')) == 0

    def test_like_birth(self):
        user1 = mixer.blend(get_user_model())
        birth = mixer.blend(Birth)

        if not self.user.is_authenticated:
            pass
        else:
            result = self.client.execute(
                query=queries.LIKE_BIRTH,
                variables={
                    'id': birth.pk,
                    'email': user1.email,
                }
            )
            assert not result.errors
            assert birth.likes == 1

            user2 = mixer.blend(get_user_model())
            self.client.execute(
                query=queries.LIKE_BIRTH,
                variables={
                    'id': birth.pk,
                    'email': user2.email,
                }
            )
            assert birth.likes == 2

            self.client.execute(
                query=queries.LIKE_BIRTH,
                variables={
                    'id': birth.pk,
                    'email': user2.email,
                }
            )
            assert birth.likes == 1


class TestAnonymousClient(BaseClass):
    @classmethod
    def setup(cls):
        cls.client = JSONWebTokenClient()
        cls.user = AnonymousUser()


class TestAuthenticationClient(BaseClass):
    @classmethod
    def setup(cls):
        cls.client = JSONWebTokenClient()
        cls.user = mixer.blend(get_user_model())

        cls.client.authenticate(cls.user)
