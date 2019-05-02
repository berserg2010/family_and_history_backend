import graphene
import graphql_jwt

import auth_app.schema as auth_app
import person_app.schema as person_app_schema
import family_app.schema as family_app_schema


class Query(
    auth_app.Query,
    person_app_schema.Query,
    family_app_schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    auth_app.Mutation,
    person_app_schema.Mutation,
    family_app_schema.Mutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
