import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from graphql_jwt.testcases import JSONWebTokenClient

from .. import schema
from . import queries


pytestmark = pytest.mark.django_db


class TestUser:
    def test_user_type(self):
        instance = schema.UserType()
        assert instance

    def test_signup_user_and_current_user(self):
        client = JSONWebTokenClient()
        variable = {'email': 'petrov@gmail.ru', 'password': '1234'}

        result = client.execute(query=queries.SIGNUP_USER, variables=variable)
        tkn1 = result.data.get('tokenAuth')['token']
        assert not result.errors

        variable = {'email': 'petro@gmail.ru', 'password': '1234'}
        result = client.execute(queries.TOKEN_AUTH, variables=variable)
        assert result.errors
        variable = {'email': 'petrov@gmail.ru', 'password': '124'}
        result = client.execute(queries.TOKEN_AUTH, variables=variable)
        assert result.errors

        variable = {'email': 'petrov@gmail.ru', 'password': '1234'}
        result = client.execute(queries.TOKEN_AUTH, variables=variable)
        assert result.data.get('tokenAuth')['token'] and not result.errors
        assert tkn1 == result.data.get('tokenAuth')['token']

        result = client.execute(queries.CURRENT_USER)
        assert result.data.get('currentUser') is None

        client.authenticate(get_user_model().objects.get(email=variable['email']))
        result = client.execute(queries.CURRENT_USER)
        assert result.data.get('currentUser')['email'] == variable['email']

    def test_resolve_all_users(self):
        mixer.blend(get_user_model())
        mixer.blend(get_user_model())
        client = JSONWebTokenClient()

        result = client.execute(queries.ALL_USER)
        assert len(result.data.get('allUsers')) == 2, 'Should return all users'
