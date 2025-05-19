# GraphQL Schema autogeneration

import logging
from collections.abc import Callable, Iterator
from enum import Enum
from typing import Any, TypedDict, cast

import graphene
from django.apps import apps
from django.db.models import Model as DjangoModel
from graphene.types.base import BaseType

from senjor.models.base import GQLModel
from senjor.models.fields.types import FieldStruct, GQLSchemaType


# types
class AccessControl(Enum):
    PRIVATE = 0
    PUBLIC = 1
    PROTECTED = 2


class ActionType(TypedDict):
    mutation: Callable[..., Any] | str | None
    subscription: Callable[..., Any] | str | None
    query: Callable[..., Any] | str | None


# Root Object Types management
class GQLRootSchema:
    """
    Handles the root object types meaning a singleton instance for Query, Mutation, Subscription. All others ObjectTypes must inherit from GQLObjectType instead.

    """

    _gql_fields: FieldStruct = (
        {  # this are the our own custom set of fields, this arent graphene.Field types so is just for internal usage of the Senjor framework
            "query": {},
            "mutation": {},
            "subscription": {},
            "general": {},
        }
    )

    def __init__(
        self,
    ) -> None:
        self.__initialized: bool = False
        self.__query_object_type: type[graphene.ObjectType] | None = None
        self.__mutation_object_type: type[graphene.ObjectType] | None = None
        self.__subscription_object_type: type[graphene.ObjectType] | None = None

    def model_to_schema(
        self, model: DjangoModel, operation_type: GQLSchemaType = "query"
    ) -> graphene.ObjectType | None:
        return self._gql_fields.get(operation_type, {}).get(
            model._meta.object_name, None  # type: ignore
        )

    def __initialize(
        self,
    ):
        """
        Populates our internal Schema struct to organize the fields
        """
        if not self.__initialized:
            logging.debug("Initializing schema...")
            for app_config in apps.get_app_configs():
                logging.debug(f"Processing app {app_config}")
                models: Iterator[type[GQLModel] | type[DjangoModel]] = (
                    app_config.get_models()
                )
                logging.debug(f"Senjor autodetected models are: {models}")
                for model in models:
                    if issubclass(model, GQLModel):
                        self._gql_fields[model.get_gql_operation_type()][
                            model.get_gql_name()
                        ] = model
                logging.debug(f"Schema struct generated {self._gql_fields}")
            self.__initialized = True
        else:
            logging.debug("Schema already initialized skipping instead")

    def __get_object_type(self, gql_type: GQLSchemaType) -> type[graphene.ObjectType]:
        fields: dict[str, BaseType] = dict(
            [
                (field_item[0], field_item[1].get_gql_field(gql_type))
                for field_item in (
                    cast(
                        dict[str, GQLModel],
                        self._gql_fields[gql_type] | self._gql_fields["general"],
                    )
                ).items()
            ]
        )
        object_type: type[graphene.ObjectType] = type(
            f"Base{gql_type.title()}", (graphene.ObjectType,), fields
        )
        logging.debug(
            "Gonna create root ObjectType with name Base%s that have fields %s and it looks like %s",
            gql_type.title(),
            fields,
            object_type,
        )
        return object_type

    def __generate_query_type(
        self,
    ) -> type[graphene.ObjectType]:
        logging.debug("Senjor: Generating Query ObjectType")
        if not self.__query_object_type:
            self.__query_object_type = self.__get_object_type("query")
        return self.__query_object_type

    def __generate_mutation_type(
        self,
    ) -> type[graphene.ObjectType]:
        logging.debug("Senjor: Generating Mutation ObjectType")
        if not self.__mutation_object_type:
            self.__mutation_object_type = self.__get_object_type("mutation")
        return self.__mutation_object_type

    def __generate_subscription_type(
        self,
    ) -> type[graphene.ObjectType]:
        logging.debug("Senjor: Generating Subscription ObjectType")
        if not self.__subscription_object_type:
            self.__subscription_object_type = self.__get_object_type("subscription")
        return self.__subscription_object_type

    @property
    def value(
        self,
    ):
        self.__initialize()

        return graphene.Schema(
            query=(
                self.__generate_query_type()
                if self._gql_fields["general"] or self._gql_fields["query"]
                else None
            ),
            mutation=(
                self.__generate_mutation_type()
                if self._gql_fields["general"] or self._gql_fields["mutation"]
                else None
            ),
            subscription=(
                self.__generate_subscription_type()
                if self._gql_fields["general"] or self._gql_fields["subscription"]
                else None
            ),
        )

    def __getattribute__(self, name: str):
        try:
            value = super().__getattribute__(name)
        except AttributeError:
            value = super().__getattribute__("value")
            value = value.__getattribute__(name)
        return value

    @property
    def __class__(cls) -> type[graphene.Schema]:  # type: ignore
        """"""
        return graphene.Schema  # Make Graphene to think this is a graphene.Schema

    def __dict__(  # type: ignore
        self,
    ):
        return self._gql_fields

    def __repr__(
        self,
    ):
        return str(self._gql_fields)
