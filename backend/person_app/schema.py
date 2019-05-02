import graphene

from .person import schema as person_schema
from .events.birth import schema as birth_schema


class Query(
    person_schema.Query,
    birth_schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    person_schema.Mutation,
    birth_schema.Mutation,
    graphene.ObjectType,
):
    pass
