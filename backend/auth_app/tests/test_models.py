import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer


pytestmark = pytest.mark.django_db


def test_create_user():
    user = mixer.blend(get_user_model())
    assert user.pk > 0
