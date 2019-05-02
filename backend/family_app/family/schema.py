import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
import json

from person_app.models import Birth
from person_app.events.birth.schema import BirthType
from .models import Family, Child


# Family
class FamilyType(DjangoObjectType):
    class Meta:
        model = Family


class FamilyInput(graphene.InputObjectType):
    id = graphene.ID()
    note = graphene.String()


class SaveFamilyMutation(graphene.Mutation):
    status = graphene.Int()
    formErrors = graphene.String()
    family = graphene.Field(FamilyType)

    class Arguments:
        data = FamilyInput()

    def mutate(self, info, data=None, **kwargs):
        if not info.context.user.is_authenticated:
            return SaveFamilyMutation(status=403)

        if info.context.user:
            user = info.context.user
        else:
            user = None

        if data.get('id') and Family.objects.filter(pk=data.get('id')):
            family = Family.objects.get(pk=data.get('id'))
            family.note = data.get('note')
            family.changer = user
            family.save()
        else:
            family = Family.objects.create(
                note=data.get('note'),
                submitter=user,
            )

        return SaveFamilyMutation(
            status=200,
            family=family,
        )


class DeleteFamilyMutation(graphene.Mutation):
    status = graphene.Int()
    formErrors = graphene.String()
    id = graphene.ID()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, **kwargs):
        if not info.context.user.is_authenticated:
            return DeleteFamilyMutation(status=403)

        id = kwargs.get('id')

        if id is None:
            return DeleteFamilyMutation(
                status=400,
                formErrors=json.dumps(
                    {'id': ['Please enter an id']}
                )
            )

        if Family.objects.filter(pk=id).exists():
            Family.objects.get(pk=id).delete()

        return DeleteFamilyMutation(
            status=200,
            id=id,
        )


# Child
class ChildType(DjangoObjectType):
    family = graphene.Field(FamilyType)
    birth = graphene.Field(BirthType)

    class Meta:
        model = Child
        exclude_fields = (
            '_family',
            '_birth',
        )


class ChildInput(graphene.InputObjectType):
    id = graphene.ID()
    idFamily = graphene.ID()
    idBirth = graphene.ID()
    reltofath = graphene.String()
    reltomoth = graphene.String()
    childnbrfath = graphene.Int()
    childnbrmoth = graphene.Int()


class SaveChildMutation(graphene.Mutation):
    status = graphene.Int()
    formErrors = graphene.String()
    child = graphene.Field(ChildType)

    class Arguments:
        data = ChildInput()

    def mutate(self, info, data=None, **kwargs):
        if not info.context.user.is_authenticated:
            return SaveChildMutation(status=403)

        # if info.context.user:
        #     user = info.context.user
        # else:
        #     user = None

        id = data.get('id')

        if id and Child.objects.filter(pk=id):
            child = Child.objects.get(pk=id)
            child.family = data.get('idFamily')
            child.birth = data.get('idBirth')
            # child.changer = user
        else:
            child = Child.objects.create(
                family=data.get('idFamily'),
                birth=data.get('idBirth'),
                # submitter=user,
            )

        child.reltofath = data.get('reltofath')
        child.reltomoth = data.get('reltomoth')
        child.childnbrfath = data.get('childnbrfath')
        child.childnbrmoth = data.get('childnbrmoth')
        # child.changer = user
        child.save()

        return SaveChildMutation(
            status=200,
            child=child,
        )


class DeleteChildMutation(graphene.Mutation):
    status = graphene.Int()
    formErrors = graphene.String()
    id = graphene.ID()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, **kwargs):
        if not info.context.user.is_authenticated:
            return DeleteChildMutation(status=403)

        id = kwargs.get('id')

        if id is None:
            return DeleteChildMutation(
                status=400,
                formErrors=json.dumps(
                    {'id': ['Please enter an id']}
                )
            )

        if Child.objects.filter(pk=id).exists():
            Child.objects.get(pk=id).delete()

        return DeleteChildMutation(
            status=200,
            id=id,
        )


class Query(graphene.ObjectType):
    all_family = graphene.List(
        FamilyType,
    )

    family = graphene.Field(
        FamilyType,
        id=graphene.ID(),
    )

    all_child = graphene.List(
        ChildType,
        idFamily=graphene.ID()
    )

    child = graphene.Field(
        ChildType,
        id=graphene.ID(),
    )

    # @login_required
    def resolve_all_family(self, info, **kwargs):
        return Family.objects.all().order_by('-changed')

    def resolve_family(self, info, **kwargs):
        id = kwargs.get('id')
        return Family.objects.get(pk=id)

    def resolve_all_child(self, info, **kwargs):
        id_family = kwargs.get('idFamily')
        if id_family:
            return Child.objects.filter(_family=id_family)
        else:
            return Child.objects.all()

    def resolve_child(self, info, **kwargs):
        id = kwargs.get('id')
        return Child.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    save_family = SaveFamilyMutation.Field()
    delete_family = DeleteFamilyMutation.Field()
    save_child = SaveChildMutation.Field()
    delete_child = DeleteChildMutation.Field()
