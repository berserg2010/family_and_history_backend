import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from ..models import Family, Child
from person_app.models import Birth
from core.models import (
    DateTime,
    GivName,
    SurName,
    SURNAME_DICT,
)

pytestmark = pytest.mark.django_db


class TestFamily:
    def test_family(self):
        instance = mixer.blend(Family)
        assert instance
        assert instance.pk


class TestChild:
    def test_child(self):
        instance = mixer.blend(Child)
        assert instance
        assert instance.pk

        brd1 = mixer.blend(Birth)
        fml1 = mixer.blend(Family)
        cld1 = Child(birth=brd1,
                     family=fml1,
                     childnbrfath=1,
                     childnbrmoth=1
                     )
        cld1.save()
        assert cld1
        assert fml1.child.all().count() == 1

        brd2 = mixer.blend(Birth)
        fml1.child.add(brd2,
                       through_defaults={
                           'childnbrfath': 2,
                           'childnbrmoth': 2,
                       })
        assert fml1.child.all().count() == 2

        cld2 = Child.objects.get(_family=fml1, _birth=brd2)
        assert cld2.childnbrfath == 2
