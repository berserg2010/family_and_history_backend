import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
import json

from .models import Birth
from core.schema import (
    EventFieldType,
    EventFieldInput,
    exclude_fields_event_field,
)
from person_app.person.schema import PersonType


class BirthType(
    EventFieldType,
    # DjangoObjectType,
):
    person = graphene.Field(PersonType)
    givname = graphene.String()
    surname = graphene.String()

    class Meta:
        model = Birth
        filter_fields = {'_surname': ['icontains']}
        exclude_fields = exclude_fields_event_field + (
            '_person',
            '_givname',
            '_surname',
        )


class BirthInput(
    EventFieldInput,
    graphene.InputObjectType,
):
    idPerson = graphene.ID()
    gender = graphene.String()
    givname = graphene.String()  # Может быть GivName
    surname = graphene.String()  # Может быть SurName


def is_data(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if value:
                return True


class SaveBirthMutation(graphene.Mutation):
    status = graphene.Int()
    formErrors = graphene.String()
    birth = graphene.Field(BirthType)

    class Arguments:
        data = BirthInput()

    def mutate(self, info, data=None, **kwargs):
        if not info.context.user.is_authenticated:
            return SaveBirthMutation(status=403)

        if not is_data(data):
            return SaveBirthMutation(
                status=400,
                formErrors=json.dumps(
                    {'data': ['Please enter a some data']}
                )
            )

        if info.context.user:
            user = info.context.user
        else:
            user = None

        id = data.get('id')

        if id and Birth.objects.filter(pk=id):
            birth = Birth.objects.get(pk=id)
            birth.changer = user

        else:
            birth = Birth.objects.create(
                pk=id,
                submitter=user,
                person=data.get('idPerson')
            )

        birth.gender = data.get('gender', 'U')
        birth.givname = data.get('givname')
        birth.surname = data.get('surname')
        birth.datetime = {
            'day': data.get('day'),
            'month': data.get('month'),
            'year': data.get('year'),
            'hour': data.get('hour'),
            'minute': data.get('minute'),
        }
        birth.note = data.get('note')
        birth.save()

        return SaveBirthMutation(
            status=200,
            birth=birth,
        )


class DeleteBirthMutation(graphene.Mutation):
    status = graphene.Int()
    formErrors = graphene.String()
    id = graphene.ID()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, **kwargs):
        if not info.context.user.is_authenticated:
            return DeleteBirthMutation(status=403)

        id = kwargs.get('id')

        if id is None:
            return DeleteBirthMutation(
                status=400,
                formErrors=json.dumps(
                    {'id': ['Please enter an id']}
                )
            )

        if Birth.objects.filter(pk=id).exists():
            Birth.objects.get(pk=id).delete()

        return DeleteBirthMutation(
            status=200,
            id=id,
        )


class LikeBirthMutation(graphene.Mutation):
    status = graphene.Int()
    formErrors = graphene.String()
    birth = graphene.Field(BirthType)

    class Arguments:
        id = graphene.ID(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        # if not info.context.user.is_authenticated:
        #     return LikeBirthMutation(status=403)

        id = kwargs.get('id')
        email = kwargs.get('email')
        user = get_user_model().objects.get(email=email)
        birth = Birth.objects.get(pk=id)

        if Birth.objects.filter(_person=birth.person, _likes=user).exists():
            birth._likes.remove(user)
        else:
            birth._likes.add(user)

        return LikeBirthMutation(
            status=200,
            birth=birth,
        )


# Output
class Query(graphene.ObjectType):
    all_birth = graphene.List(
        BirthType,
        idPerson=graphene.ID()
    )

    birth = graphene.Field(
        BirthType,
        id=graphene.ID(),
    )

    search_birth = graphene.List(
        BirthType,
        searchTerm=graphene.String(),
    )

    # @login_required
    def resolve_all_birth(self, info, **kwargs):
        id_person = kwargs.get('idPerson')
        if id_person:
            return Birth.objects.filter(_person=id_person).order_by('-changed')
        else:
            return Birth.objects.all().order_by('-changed')

    def resolve_birth(self, info, **kwargs):
        id = kwargs.get('id')
        return Birth.objects.get(pk=id)

    def resolve_search_birth(self, info, **kwargs):
        return Birth.objects.filter(  # Фильтр только по surname_male?
            _surname___surname_male__icontains=kwargs.get('searchTerm')
        ).order_by('-changed')


class Mutation(graphene.ObjectType):
    save_birth = SaveBirthMutation.Field()
    delete_birth = DeleteBirthMutation.Field()
    like_birth = LikeBirthMutation.Field()
