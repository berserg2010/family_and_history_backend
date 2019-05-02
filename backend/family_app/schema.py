import graphene

from .family import schema as family_schema
from .events.marriage import schema as marriage_schema


class Query(
    family_schema.Query,
    marriage_schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    family_schema.Mutation,
    marriage_schema.Mutation,
    graphene.ObjectType,
):
    pass
