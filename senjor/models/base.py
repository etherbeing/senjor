import logging
from typing import Any, Self, cast

import graphene
from django.db import models
from django.db.models.signals import post_save
from graphene.types.base import BaseType
from graphql import FieldNode, GraphQLResolveInfo

from senjor.core.exceptions import GQLBaseException
from senjor.models.fields.base import GQLField
from senjor.models.fields.types import FieldStruct, GQLSchemaType


class GQLModelMeta(models.base.ModelBase):
    _gql_fields: FieldStruct = (
        {  # static field to automatically handle caching on memory of the models  # this are the our own custom set of fields, this arent graphene.Field types so is just for internal usage of the Senjor framework
            "query": {},
            "mutation": {},
            "subscription": {},
            "general": {},
        }
    )

    def __new__(cls, name: str, bases: tuple[type[Any]], attrs: dict[str, Any]):
        instance: GQLModelMeta | None = cls._gql_fields[
            attrs.get("schema_type", "query")
        ].get(name, None)
        if not instance:
            instance = super().__new__(cls, name, bases, attrs)
            if not instance._meta.abstract:  # type: ignore
                logging.debug(
                    "New instance for model %s is being created",
                    instance._meta.model_name,  # type: ignore
                )
                instance._gql_args = {}  # type: ignore
                cls._gql_fields[attrs.get("schema_type", "query")][name] = instance
        return instance


class GQLModel(models.Model, metaclass=GQLModelMeta):
    """
    Define your GraphQL Schema and DB all in one, avoiding repeating each field declaration here and in the graphql element
    """

    # _cached_struct:
    is_singleton: bool = False
    schema_type: GQLSchemaType = "query"

    _gql_object_type: graphene.Field | None = None
    _gql_schema_type: GQLSchemaType = "query"  # default it to "general instead"
    _gql_args: dict[str, graphene.Argument] = (
        {}
    )  # This is not used as static as it seems the GQLModelMeta make it instance dependant

    @classmethod
    def get_gql_object_type(cls, discard_related_from: Self | None = None):
        if not cls._gql_object_type:
            cls.__generate_object_type(discard_related_from)
        return cls._gql_object_type

    @classmethod
    def get_gql_name(
        cls,
    ):
        return cls._meta.model_name or cls.__class__.__name__

    @classmethod
    def check(cls, **kwargs: dict[str, Any]):
        cls.__generate_object_type()
        return super().check(**kwargs)

    @classmethod
    def __generate_object_type(cls, discard_related_from: Self | None = None):
        logging.debug(f"Generating schema type for model {cls.get_gql_name()}")
        gql_fields: dict[str, graphene.Field] = {}
        for field in cls._meta.get_fields(True, False):
            # TODO Actually all fields aren't GQLField some are GQLRelatedFields which are handled slightly (totally) differently, so we must unify them
            gql_fields[cast(GQLField, field).name] = GQLField.to_gql_field(
                field,
                cls._gql_schema_type,
                cls,
                discard_related_from=cast(models.Model, discard_related_from),
            )
            # ignore else states as are not supported fields yet
        cls._gql_object_type = cls.__get_gql_field(
            gql_fields,
        )
        logging.debug(
            "Generated ObjectType for model %s: %s, fields: %s",
            cls.get_gql_name(),
            cls._gql_schema_type,
            gql_fields,
        )

    @classmethod
    def __get_gql_field(cls, fields: dict[str, graphene.Field]):
        if cls._gql_object_type is None:
            # NOTE: Queries always use graphene.Field
            cls._gql_object_type = graphene.Field(
                type(
                    cls.get_gql_name(),
                    (graphene.ObjectType,),
                    fields,
                ),
                description=cls.__doc__,
                resolver=cls.__default_resolver,
                name=cls.get_gql_name(),
                args=cls.__get_args(),
            )
            logging.debug(
                "GQLModel: name: %s, fields: %s, content: %s",
                cls.get_gql_name(),
                fields,
                cls._gql_object_type.__dict__,
            )
        return cls._gql_object_type

    @classmethod
    def __get_args(cls):
        for field in cls._meta.get_fields():
            if field.is_relation:  # type: ignore
                pass
            else:
                cls._gql_args.update(
                    {
                        field.name: graphene.Argument(  # type:ignore
                            type(GQLField.to_gql_field(field, cls.schema_type, cls)),
                            name=field.name,  # type:ignore
                            required=False,
                        )
                    }
                )
        return cls._gql_args

    @classmethod
    def get_gql_field(cls, gql_type: GQLSchemaType) -> BaseType:
        logging.debug('Obtaining the field for the schema type: "%s"', gql_type)
        cls._gql_schema_type = gql_type
        if not cls._gql_object_type:
            cls.__generate_object_type()
        logging.debug("Schema type field %s generated...", cls._gql_object_type)
        return cast(BaseType, cls._gql_object_type)

    @classmethod
    def get_gql_operation_type(
        cls,
    ) -> GQLSchemaType:
        return cls._gql_schema_type

    @classmethod
    def __default_resolver(
        cls,
        *args: list[Any],
        **kwargs: dict[str, Any],
    ) -> list[BaseType] | BaseType:
        """
        Default query resolver for GraphQL object types
        """
        info: GraphQLResolveInfo | None = None
        for arg in args:
            if isinstance(arg, GraphQLResolveInfo):
                info = arg
                break
        else:
            raise GQLBaseException("No info object given")

        model_object_type = cls.get_gql_field("query").type  # type: ignore
        logging.debug(
            "Resolving query with args %s and kwargs %s, and info %s",
            args,
            kwargs,
            info,
        )
        request_fields: dict[str, str] = (
            {}
        )  # keys are the ObjectType fields's names and the values are the models's name
        for field in cast(list[FieldNode], info.field_nodes[0].selection_set.selections):  # type: ignore
            if hasattr(field, "name"):
                field_value: GQLField = cast(
                    GQLField, cls._meta.get_field(field.name.value)
                )
                related_model: GQLModel | models.Model | None = (
                    field_value.related_model
                )
                if related_model and not issubclass(
                    field_value.related_model, GQLModel
                ):
                    request_fields[
                        f"{field.name.value}_{field_value.related_model._meta.pk.name}"
                    ] = field.name.value
                else:
                    request_fields[field.name.value] = field.name.value

        logging.debug("Request Fields, plus models fields: %s", request_fields)
        model_rows: models.QuerySet[Self] = cls.objects.filter(**kwargs).only(
            *request_fields.keys()
        )

        if model_rows.count() > 1:
            rows: list[BaseType] = []
            for row in model_rows:
                row_args: dict[str, graphene.Argument] = dict(
                    [
                        (request_fields[item[0]], item[1])
                        for item in row.__dict__.items()
                        if item[0] in request_fields.keys()
                    ]
                )
                rows.append(model_object_type(**row_args))  # type:ignore
            return rows
        else:
            result: models.Model | None = (
                model_rows.first()
            )  # use a serializer like the one from DRF for now lets just do the next
            if not result:
                return model_object_type()  # type: ignore

            result_args = dict(
                [
                    (request_fields[item[0]], item[1])
                    for item in result.__dict__.items()
                    if item[0] in request_fields.keys()
                ]
            )
            logging.info("Requested fields are %s", request_fields)
            logging.debug("Result Args: %s", result_args)
            logging.debug(
                "DB query result: %s with dict fields %s", result, result.__dict__
            )
            logging.debug("GQLField: %s", model_object_type)  # type: ignore
            return model_object_type(**result_args)  # type:ignore

    @classmethod
    def __default_mutation(  # type: ignore[reportUnusedFunction]
        cls,
        root: Any,
        info: GraphQLResolveInfo,
        *args: list[Any],
        **kwargs: dict[str, Any],
    ) -> list[BaseType] | BaseType:
        return type(cls.get_gql_field(gql_type="mutation"))()

    @classmethod
    async def __default_subscriber(  # type: ignore[reportUnusedFunction]
        cls,
        root: Any,
        info: GraphQLResolveInfo,
        *args: list[Any],
        **kwargs: dict[str, Any],
    ) -> list[BaseType] | BaseType:
        return type(cls.get_gql_field("subscription"))()

    class Meta:
        abstract = True


def __channel_sync(sender: GQLModel, instance: GQLModel, **kwargs: dict[str, Any]):
    logging.debug("Syncing live channel after model update")


post_save.connect(__channel_sync, GQLModel, weak=False)
