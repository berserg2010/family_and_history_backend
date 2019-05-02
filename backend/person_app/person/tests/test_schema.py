import pytest
from mixer.backend.django import mixer

from abc import ABC

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from graphql_jwt.testcases import JSONWebTokenClient

from person_app.person import schema
from person_app.person.models import Person
from . import queries


pytestmark = pytest.mark.django_db


def test_person_type():
    instance = schema.PersonType()
    assert instance


class BaseClass(ABC):
    def test_all_person(self):
        mixer.blend(Person)
        mixer.blend(Person)
        result = self.client.execute(query=queries.ALL_PERSON)
        assert len(result.data.get('allPerson')) == 2, 'Should return all person'

    def test_person(self):
        person = mixer.blend(Person)
        result = self.client.execute(
            query=queries.PERSON,
            variables={'id': person.pk}
        )
        assert not result.errors
        assert result.data.get('person')['id'] == str(person.pk)

    def test_save_person_mutation(self):
        note = [[None, ':)'], [1, ':(']]

        for i in note:
            VARIABLE = {
                "data": {
                    "id": i[0],
                    "note": i[1]
                },
            }

            result = self.client.execute(
                query=queries.SAVE_PERSON,
                variables=VARIABLE,
            )
            assert not result.errors

            if not self.user.is_authenticated:
                assert result.data.get('savePerson')['status'] == 403, 'Should return 403 if user is not logged in'
            else:
                assert result.data.get('savePerson')['status'] == 200, 'Should return 200 if mutation is successful'
                person_id = int(result.data.get('savePerson')['person']['id'])
                assert person_id == 1, 'Should create new person'
                person = Person.objects.get(pk=person_id)
                assert person.note == VARIABLE.get('data')['note']

    def test_delete_person_mutation(self):
        person = mixer.blend(Person)

        if not self.user.is_authenticated:
            result = self.client.execute(
                query=queries.DELETE_PERSON,
                variables={'id': person.pk}
            )
            assert not result.errors
            assert result.data.get('deletePerson')['status'] == 403, 'Should return 403 if user is not logged in'
        else:
            result = self.client.execute(query=queries.DELETE_PERSON)
            assert result.errors

            result = self.client.execute(query=queries.DELETE_PERSON, variables={'id': person.pk})
            assert not result.errors
            assert result.data.get('deletePerson')['status'] == 200, 'Should return 200 if mutation is successful'


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
