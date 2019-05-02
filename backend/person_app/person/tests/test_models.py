import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
import re

from ..models import Person
from core.models import (
    DateTime,
    GivName,
    SurName,
    SURNAME_DICT,
)

pytestmark = pytest.mark.django_db


# Person
class TestPerson:
    def test_person(self):
        assert mixer.blend(Person)
