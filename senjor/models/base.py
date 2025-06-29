# For some reason it seems that the subscription is calling some field or perhaps is due to calling get_fields or the other methods on the initializer
# don't know but is "raising You cannot call this from an async context - use a thread or sync_to_async." then we need to do something about it
# FIXME: Subscriptions aren't displaying the values to the backend for some reason, as the resolver is made perhaps the problem is if GraphQL tries to
# call the ObjectType resolver if returns None as cls() and at that point is instantiating the models.Model which is not async safe.

import logging
from typing import Any, TypedDict, cast

import strawberry
from django.db import models
from django.db.models.signals import post_save
from strawberry.types.base import StrawberryType
from strawberry.types.field import StrawberryField

from senjor.models.fields.base import GQLField
from senjor.models.fields.types import GQLSchemaType

DEFAULT_SCHEMA_TYPES: list[GQLSchemaType] = ["query", "mutation", "subscription"]


class GenericDict(TypedDict):
    id: int


class GQLModelMeta(models.base.ModelBase):

    def __new__(cls, name: str, bases: tuple[type[Any]], attrs: dict[str, Any]):
        """
        Here we autogenerates all the schemas configured for this GQLModel
        """
        gql_model: GQLModel = super().__new__(cls, name, bases, attrs)  # type: ignore
        gql_model._senjor_field = None  # type: ignore
        return gql_model


class GQLModel(models.Model, metaclass=GQLModelMeta):
    """
    Define your GraphQL Schema and DB all in one, avoiding repeating each field declaration here and in the graphql element
    """

    _senjor_field: StrawberryField | None = None

    @classmethod
    def get_senjor_name(cls):
        return cls._meta.model_name or cls.__class__.__name__

    @classmethod
    def get_senjor_description(cls):
        return cls.__doc__ or cls._meta.verbose_name

    @classmethod
    def get_senjor_field(
        cls,
    ):
        if not cls._senjor_field:
            fields: dict[str, Any] = {}
            for field in cls._meta.get_fields(
                include_parents=True, include_hidden=False
            ):
                if isinstance(field, GQLField):
                    fields[field.get_senjor_name()] = (
                        field.get_senjor_field()
                    )  # is not self.get)senjor_field but rather the one from the field
                else:
                    senjor_version: GQLField = GQLField.native_to_senjor_field(field)  # type: ignore
                    fields[senjor_version.get_senjor_name()] = (
                        senjor_version.get_senjor_field()
                    )
            field = type(
                cls.get_senjor_name(),
                (),
                fields,
            )

            _senjor_field = cast(
                StrawberryType,
                strawberry.type(
                    name=cls.get_senjor_name(),
                    description=cls.get_senjor_description(),
                )(field),
            )
            cls.resolve.__annotations__.update(
                {"return": _senjor_field}
            )  # annotate this model resolve function to have the return type expected by strawberry
            cls._senjor_field = cast(
                StrawberryField,
                strawberry.field(
                    resolver=cls.resolve,
                ),
            )
        return cls._senjor_field

    @classmethod
    async def resolve(
        cls,
        info: strawberry.Info,
    ):
        gql_model_field = cls.get_senjor_field()
        fields: dict[str, StrawberryField] = cast(dict[str, StrawberryField], gql_model_field.type_annotation.annotation.__dataclass_fields__)  # type: ignore
        element = await cls.objects.afirst()
        for field_name in fields:
            fields[field_name].instance = element  # type: ignore
        return cast(StrawberryType, gql_model_field.resolve_type())

    class Meta:
        abstract = True


def __channel_sync(sender: GQLModel, instance: GQLModel, **kwargs: dict[str, Any]):
    logging.debug("Syncing live channel after model update")


post_save.connect(__channel_sync, GQLModel, weak=False)
