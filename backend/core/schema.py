import graphene
from graphene_django import DjangoObjectType

from .models import *


# DateTime
class DateTimeType(DjangoObjectType):
    class Meta:
        model = DateTime
        exclude_fields = (
            'qualifiers',
            'calendar',
            'link',
        )


class DateTimeInput(graphene.InputObjectType):
    day = graphene.Int()
    month = graphene.Int()
    year = graphene.Int()
    hour = graphene.Int()
    minute = graphene.Int()


# GivName
class GivNameType(DjangoObjectType):
    class Meta:
        model = GivName


class GivNameInput(graphene.InputObjectType):
    givname = graphene.String()


# SurName
class SurNameType(DjangoObjectType):
    class Meta:
        model = SurName


class SurNameInput(graphene.InputObjectType):
    surname = graphene.String()


# ObjectField
class ObjectFieldInput(graphene.InputObjectType):
    note = graphene.String()


# EventField
class EventFieldType(DjangoObjectType):
    datetime = graphene.JSONString()  # Как представить dict?
    likes = graphene.Int()

    class Meta:
        abstract = True


class EventFieldInput(ObjectFieldInput):
    id = graphene.ID()
    note = graphene.String()

    day = graphene.Int()
    month = graphene.Int()
    year = graphene.Int()
    hour = graphene.Int()
    minute = graphene.Int()


exclude_fields_event_field = (
    '_datetime',
    '_likes',
    'place',
    'evidence'
)


# EventFieldTest
class EventFieldTypeTest(DjangoObjectType):
    datetime = graphene.Field(DateTimeType)
    likes = graphene.Int()

    class Meta:
        abstract = True


class EventFieldInputTest(ObjectFieldInput):
    id = graphene.ID()
    note = graphene.String()
    datetime = DateTimeInput()
