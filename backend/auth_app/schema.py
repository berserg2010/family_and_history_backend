import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class SignupUserMutation(graphene.Mutation):
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    password = graphene.String()

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        user = get_user_model()(
            first_name=kwargs.get('first_name', ''),
            last_name=kwargs.get('last_name', ''),
            email=kwargs.get('email'),
        )
        user.set_password(kwargs.get('password'))
        user.save()

        return SignupUserMutation(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )


# Output
class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    current_user = graphene.Field(UserType)

    # @login_required
    def resolve_all_users(self, info):
        return get_user_model().objects.all()

    def resolve_current_user(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            return None
        return user


class Mutation(graphene.ObjectType):
    signup_user = SignupUserMutation.Field()
