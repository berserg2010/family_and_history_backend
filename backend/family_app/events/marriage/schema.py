import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
import json

from .models import Marriage
from core.schema import (
    EventFieldType,
    EventFieldInput,
    exclude_fields_event_field,
)
from person_app.person.schema import PersonType
from family_app.family.schema import FamilyType


class MarriageType(
    EventFieldType,
    # DjangoObjectType,
):
    family = graphene.Field(FamilyType)
    husband = graphene.Field(PersonType)
    wife = graphene.Field(PersonType)
    husbname = graphene.String()
    wifename = graphene.String()

    class Meta:
        model = Marriage
        exclude_fields = exclude_fields_event_field + (
            '_family',
            '_husband',
            '_wife',
            '_husbname',
            '_wifename',
        )


class MarriageInput(
    EventFieldInput,
    # graphene.InputObjectType,
):
    idFamily = graphene.ID()
    husband = graphene.ID()
    wife = graphene.ID()
    husbname = graphene.String()  # Может быть SurName
    wifename = graphene.String()  # Может быть SurName


def is_data(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if value:
                return True


class SaveMarriageMutation(graphene.Mutation):
    status = graphene.Int()
    formErrors = graphene.String()
    marriage = graphene.Field(MarriageType)

    class Arguments:
        data = MarriageInput()

    def mutate(self, info, data, **kwargs):
        if not info.context.user.is_authenticated:
            return SaveMarriageMutation(status=403)

        if not data.get('husband') and not data.get('wife'):
            return SaveMarriageMutation(
                status=400,
                formErrors=json.dumps(
                    {'data': ['Please enter husband or wife']}
                )
            )

        if info.context.user:
            user = info.context.user
        else:
            user = None

        id = data.get('id')

        if id and Marriage.objects.filter(pk=id):
            marriage = Marriage.objects.get(pk=id)
            marriage.changer = user

        else:
            marriage = Marriage.objects.create(
                # pk=id,
                submitter=user,
                family=data.get('idFamily')
            )
        marriage.husband = data.get('husband')
        marriage.wife = data.get('wife')
        marriage.husbname = data.get('husbname')
        marriage.wifename = data.get('wifename')

        marriage.datetime = {
            'day': data.get('day'),
            'month': data.get('month'),
            'year': data.get('year'),
            'hour': data.get('hour'),
            'minute': data.get('minute'),
        }
        marriage.note = data.get('note')
        marriage.save()

        return SaveMarriageMutation(
            status=200,
            marriage=marriage,
        )


class DeleteMarriageMutation(graphene.Mutation):
    status = graphene.Int()
    formErrors = graphene.String()
    id = graphene.ID()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, **kwargs):
        if not info.context.user.is_authenticated:
            return DeleteMarriageMutation(status=403)

        id = kwargs.get('id')

        if id is None:
            return DeleteMarriageMutation(
                status=400,
                formErrors=json.dumps(
                    {'id': ['Please enter an id']}
                )
            )

        if Marriage.objects.filter(pk=id).exists():
            Marriage.objects.get(pk=id).delete()

        return DeleteMarriageMutation(
            status=200,
            id=id,
        )


class LikeMarriageMutation(graphene.Mutation):
    status = graphene.Int()
    formErrors = graphene.String()
    marriage = graphene.Field(MarriageType)

    class Arguments:
        id = graphene.ID(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        # if not info.context.user.is_authenticated:
        #     return LikeMarriageMutation(status=403)

        id = kwargs.get('id')
        email = kwargs.get('email')
        user = get_user_model().objects.get(email=email)
        marriage = Marriage.objects.get(pk=id)

        if Marriage.objects.filter(_family=marriage.family, _likes=user).exists():
            marriage._likes.remove(user)
        else:
            marriage._likes.add(user)

        return LikeMarriageMutation(
            status=200,
            marriage=marriage,
        )


# Output
class Query(graphene.ObjectType):
    all_marriage = graphene.List(
        MarriageType,
        idFamily=graphene.ID()
    )

    marriage = graphene.Field(
        MarriageType,
        id=graphene.ID(),
    )

    # @login_required
    def resolve_all_marriage(self, info, **kwargs):
        id_family = kwargs.get('idFamily')
        if id_family:
            return Marriage.objects.filter(_family=id_family).order_by('-changed')
        else:
            return Marriage.objects.all().order_by('-changed')

    def resolve_marriage(self, info, **kwargs):
        id = kwargs.get('id')
        return Marriage.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    save_marriage = SaveMarriageMutation.Field()
    delete_marriage = DeleteMarriageMutation.Field()
    like_marriage = LikeMarriageMutation.Field()
