import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer

from abc import ABC

from graphql_jwt.testcases import JSONWebTokenClient

from person_app.models import Person
from family_app.family.models import Family
from family_app.events.marriage.models import Marriage
from .. import schema
from . import queries


pytestmark = pytest.mark.django_db


def test_marriage_type():
    instance = schema.MarriageType()
    assert instance


class BaseClass(ABC):
    def test_all_marriage(self):
        mixer.blend(Marriage)
        family = mixer.blend(Family)
        marriage1 = mixer.blend(Marriage)
        marriage1.family = family
        marriage1.save()
        marriage2 = mixer.blend(Marriage)
        marriage2.family = family
        marriage2.save()
        result = self.client.execute(query=queries.ALL_MARRIAGE)
        assert not result.errors
        assert len(result.data.get('allMarriage')) == 3, 'Should return all marriage'

        result = self.client.execute(query=queries.ALL_MARRIAGE, variables={"idFamily": family.pk})
        assert not result.errors
        assert len(result.data.get('allMarriage')) == 2, 'Should return 2 marriage'

    def test_marriage(self):
        marriage = mixer.blend(Marriage)
        result = self.client.execute(
            query=queries.MARRIAGE,
            variables={'id': marriage.pk}
        )
        assert not result.errors
        assert result.data.get('marriage')['id'] == str(marriage.pk)

    def test_save_marriage_mutation(self):
        VARIABLE = {
            "data": {
                "husband": mixer.blend(Person).pk,
                # "wife": "",
                "husbname": "Иванов",
                "wifename": "Петрова",
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
                query=queries.SAVE_MARRIAGE,
                variables=VARIABLE,
            )
            assert not result.errors
            assert result.data.get('saveMarriage')['status'] == 403, 'Should return 403 if user is not logged in'
        else:
            result = self.client.execute(
                query=queries.SAVE_MARRIAGE,
                variables={"data": {
                    "husbname": "",
                    "wifename": "",
                    "note": "",

                    "year": None,
                    "month": None,
                    "day": None,
                    "hour": None,
                    "minute": None,
                }},
            )
            assert not result.errors
            assert result.data.get('saveMarriage')['status'] == 400

            result = self.client.execute(
                query=queries.SAVE_MARRIAGE,
                variables=VARIABLE,
            )
            assert not result.errors
            assert result.data.get('saveMarriage')['status'] == 200, 'Should return 200 if mutation is successful'
            marriage_id = int(result.data.get('saveMarriage')['marriage']['id'])
            assert marriage_id == 1, 'Should create new marriage'
            marriage = Marriage.objects.get(pk=marriage_id)
            assert marriage.husbname == VARIABLE.get('data')['husbname']
            assert marriage.wifename == VARIABLE.get('data')['wifename']
            assert marriage.submitter
            data = VARIABLE.get('data')
            assert marriage.datetime == {
                "year": data.get('year'),
                "month": data.get('month'),
                "day": data.get('day'),
                "hour": data.get('hour'),
                "minute": data.get('minute'),
            }
            assert marriage.note == VARIABLE.get('data')['note']

            VARIABLE = {
                "data": {
                    "id": marriage_id,
                    "wife": mixer.blend(Person).pk,
                    "husbname": "Петров",
                    "wifename": "Иванова",
                    "note": "",

                    "year": 1900,
                    "month": 12,
                    "day": 1,
                    "hour": 20,
                    "minute": 15,
                }
            }
            result = self.client.execute(
                query=queries.SAVE_MARRIAGE,
                variables=VARIABLE,
            )
            assert not result.errors
            assert result.data.get('saveMarriage')['status'] == 200, 'Should return 200 if mutation is successful'
            marriage_id = int(result.data.get('saveMarriage')['marriage']['id'])
            assert marriage_id == 1, 'Should create new marriage'
            marriage = Marriage.objects.get(pk=marriage_id)
            assert marriage.husbname == VARIABLE.get('data')['husbname']
            assert marriage.wifename == VARIABLE.get('data')['wifename']
            assert marriage.submitter
            data = VARIABLE.get('data')
            assert marriage.datetime == {
                "year": data.get('year'),
                "month": data.get('month'),
                "day": data.get('day'),
                "hour": data.get('hour'),
                "minute": data.get('minute'),
            }
            assert marriage.note == VARIABLE.get('data')['note']

            family = mixer.blend(Family)

            result = self.client.execute(
                query=queries.SAVE_MARRIAGE,
                variables={
                    "data": {
                        "idFamily": family.pk,
                        "wife": mixer.blend(Person).pk,
                        "husbname": "Петров",
                        "wifename": "Иванова",
                        "note": "",
                    }
                },
            )
            assert not result.errors
            assert result.data.get('saveMarriage')['status'] == 200, 'Should return 200 if mutation is successful'
            marriage_id = int(result.data.get('saveMarriage')['marriage']['id'])
            marriage = Marriage.objects.get(pk=marriage_id)
            assert marriage.family == family

    def test_delete_marriage_mutation(self):
        marriage = mixer.blend(Marriage)

        if not self.user.is_authenticated:
            result = self.client.execute(
                query=queries.DELETE_MARRIAGE,
                variables={'id': marriage.pk}
            )
            assert not result.errors
            assert result.data.get('deleteMarriage')['status'] == 403, 'Should return 403 if user is not logged in'
        else:
            result = self.client.execute(query=queries.DELETE_MARRIAGE)
            assert result.errors

            result = self.client.execute(query=queries.DELETE_MARRIAGE, variables={'id': marriage.pk})
            assert not result.errors
            assert result.data.get('deleteMarriage')['status'] == 200, 'Should return 200 if mutation is successful'

    def test_like_marriage(self):
        user1 = mixer.blend(get_user_model())
        marriage = mixer.blend(Marriage)

        if not self.user.is_authenticated:
            pass
        else:
            result = self.client.execute(
                query=queries.LIKE_MARRIAGE,
                variables={
                    'id': marriage.pk,
                    'email': user1.email,
                }
            )
            assert not result.errors
            assert marriage.likes == 1

            user2 = mixer.blend(get_user_model())
            self.client.execute(
                query=queries.LIKE_MARRIAGE,
                variables={
                    'id': marriage.pk,
                    'email': user2.email,
                }
            )
            assert marriage.likes == 2

            self.client.execute(
                query=queries.LIKE_MARRIAGE,
                variables={
                    'id': marriage.pk,
                    'email': user2.email,
                }
            )
            assert marriage.likes == 1


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
