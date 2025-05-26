# For some reason it seems that the subscription is calling some field or perhaps is due to calling get_fields or the other methods on the initializer
# don't know but is "raising You cannot call this from an async context - use a thread or sync_to_async." then we need to do something about it
# FIXME: Subscriptions aren't displaying the values to the backend for some reason, as the resolver is made perhaps the problem is if GraphQL tries to
# call the ObjectType resolver if returns None as cls() and at that point is instatiating the models.Model which is not async safe.

import asyncio
import logging
from typing import Any, Self, cast

import graphene
from django.db import models
from django.db.models.signals import post_save
from graphene.types.base import BaseType
from graphql import FieldNode, GraphQLResolveInfo

from senjor.core.exceptions import GQLBaseException
from senjor.models.fields.base import GQLField
from senjor.models.fields.types import GQLSchemaType

DEFAULT_SCHEMA_TYPES: list[GQLSchemaType] = ["query", "mutation", "subscription"]


class GQLModelMeta(models.base.ModelBase):

    def __new__(cls, name: str, bases: tuple[type[Any]], attrs: dict[str, Any]):
        """
        Here we autogenerates all the schemas configured for this GQLModel
        """
        gql_model: GQLModel = super().__new__(cls, name, bases, attrs)  # type: ignore
        gql_model._gql_args = {}  # type: ignore
        gql_model._gql_object_type_tree = {}  # type: ignore
        return gql_model


class GQLModel(models.Model, metaclass=GQLModelMeta):
    """
    Define your GraphQL Schema and DB all in one, avoiding repeating each field declaration here and in the graphql element
    """

    gql_is_singleton: bool = False
    gql_schema_type: list[GQLSchemaType] = DEFAULT_SCHEMA_TYPES

    _gql_object_type_tree: dict[GQLSchemaType, graphene.Field] = (
        {}
    )  # this is not treated as an static var is here just for easy of use perhaps declaring it in the init would be better
    _gql_args: dict[str, graphene.Argument] = (
        {}
    )  # This is not used as static as it seems the GQLModelMeta make it instance dependant

    @classmethod
    def get_gql_object_type(
        cls, schema_type: GQLSchemaType, discard_related_from: Self | None = None
    ):
        if (
            schema_type not in cls.gql_schema_type
        ):  # if this model doesnt support the given schema type
            return None
        if schema_type not in cls._gql_object_type_tree:
            cls.__generate_object_type(schema_type, discard_related_from)
        return cls._gql_object_type_tree[schema_type]

    @classmethod
    def get_gql_name(
        cls,
    ):
        return cls._meta.model_name or cls.__class__.__name__

    @classmethod
    def __generate_object_type(
        cls,
        gql_schema_type: GQLSchemaType,
        discard_related_from: Self | None = None,
    ):
        """Generate the Object Type for this model having in consideration whether or not this is for a mutation, query or subscription"""
        logging.debug(f"Generating schema type for model {cls.get_gql_name()}")
        _gql_schema_type: list[GQLSchemaType] = (
            gql_schema_type
            and [
                gql_schema_type
            ]  # if the value gql_schema (the one in the params) is set then we set it as a schema list
        ) or cls.gql_schema_type
        for schema_type in _gql_schema_type:
            gql_fields: dict[str, graphene.Field] = {}
            for field in cls._meta.get_fields(True, False):
                # TODO Actually all fields aren't GQLField some are GQLRelatedFields which are handled slightly (totally) differently, so we must unify them
                gql_fields[cast(GQLField, field).name] = GQLField.to_gql_field(
                    field,
                    schema_type,
                    cls,
                    discard_related_from=cast(models.Model, discard_related_from),
                )
                # ignore else states as are not supported fields yet
            cls._gql_object_type_tree[schema_type] = (
                cls.__get_gql_field(  # Once we got all fields we get and this OT and create a new Field
                    gql_fields, schema_type=schema_type
                )
            )
            logging.debug(
                "Generated ObjectType for model %s: %s, fields: %s",
                cls.get_gql_name(),
                schema_type,
                gql_fields,
            )

    @classmethod
    def __get_gql_field(
        cls, fields: dict[str, graphene.Field], schema_type: GQLSchemaType
    ):
        # NOTE: Queries always use graphene.Field
        if schema_type == "mutation":
            if "mutation" not in cls._gql_object_type_tree:
                mutation_instance: graphene.Mutation = cast(
                    graphene.Mutation,
                    type(
                        cls.get_gql_name(),
                        (graphene.Mutation,),
                        fields
                        | {
                            "Arguments": type("Arguments", (object,), cls.__get_args()),
                            "mutate": cls.__default_mutate,
                        },
                    ),
                )
                cls._gql_object_type_tree["mutation"] = cast(
                    graphene.Field,
                    mutation_instance.Field(  # type: ignore
                        name=cls.get_gql_name(),
                        description=cls.__doc__,
                    ),
                )
            return cls._gql_object_type_tree["mutation"]
        else:
            if schema_type not in cls._gql_object_type_tree:
                extra_fields = {}
                if schema_type == "subscription":
                    for field in fields:
                        extra_fields[f"subscribe_{field}"] = cls.__default_subscribe
                cls._gql_object_type_tree[schema_type] = graphene.Field(
                    type(
                        cls.get_gql_name(),
                        (graphene.ObjectType,),
                        fields | extra_fields,
                    ),
                    name=cls.get_gql_name(),
                    description=cls.__doc__,
                    resolver=cls.__default_resolver if schema_type == "query" else None,
                    args=cls.__get_args(),
                )
            return cls._gql_object_type_tree[schema_type]

    @classmethod
    def __get_args(cls):
        """
        Get the arguments used for this model, for example arguments for filtering or so, this args are given to the resolvers
        """
        for schema_type in cls.gql_schema_type:
            for field in cls._meta.get_fields():
                if field.is_relation:  # type: ignore
                    pass
                else:
                    cls._gql_args.update(
                        {
                            field.name: graphene.Argument(  # type:ignore
                                type(
                                    GQLField.to_gql_field(field, schema_type, cls)
                                ),  # TODO: Perhaps we'd want to handle args in a different way than fields
                                name=field.name,  # type:ignore
                                required=False,
                            )
                        }
                    )
        return cls._gql_args

    @classmethod
    def get_gql_field(cls, gql_schema_type: GQLSchemaType) -> BaseType | None:
        """
        Public function to obtain this model as the graphene.Field expected, if a mutation you'll obtain a Mutation.Field if a query you'll obtain graphene.Field(ObjectType,...) so please use this function instead of any other here for GraphQL schema generation purposes
        """
        logging.debug('Obtaining the field for the schema type: "%s"', gql_schema_type)
        if (
            gql_schema_type in cls.gql_schema_type
        ):  # if either the requested schema type is the defined one or the requested one is "general"
            if (
                gql_schema_type not in cls._gql_object_type_tree
            ):  # only process it if not already processed it
                cls.__generate_object_type(gql_schema_type=gql_schema_type)
            logging.debug(
                "Schema type field %s generated...",
                cls._gql_object_type_tree[gql_schema_type],
            )
            return cast(BaseType, cls._gql_object_type_tree[gql_schema_type])
        else:
            logging.debug(
                f'Schema type requested is not defined in this model intended schema type, if this is wrong please update the object {cls.__name__} attribute "gql_schema_type" to include "{gql_schema_type}"'
            )
            return None

    @classmethod
    def get_gql_operation_type(
        cls,
    ) -> list[GQLSchemaType]:
        return cls.gql_schema_type

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
    def __default_mutate(
        cls, _: Any, info: GraphQLResolveInfo, *args: Any, **kwargs: Any
    ):
        """
        This method is already connected to the mutations of the Senjor GQL schema
        TODO
        In the Arguments class for this mutation we should:
        - [ ] Create args named filter_by_{argname} so those tell us how to filter the models
        - [ ] This method should allow the dev to update any way he wants the db from the graphql schema, perhaps making something like an RPC here would be cool
        """
        logging.debug(f"{info}, {args}, {kwargs}")

    @classmethod
    async def __default_subscribe(
        cls, root: Any, info: GraphQLResolveInfo, *args: Any, **kwargs: Any
    ):
        """
        Default subscriber
        """
        logging.debug(f"{cls} {info}, {args}, {kwargs}")
        for i in range(5):
            yield f"Ping #{i}"
            await asyncio.sleep(1)

    @classmethod
    async def default_model_subscribe(
        cls, _: Any, info: GraphQLResolveInfo, *args: Any, **kwargs: Any
    ):
        """
        Default subscriber for the model this is being used in the Root schema as the default subscribe function for each field.

        This function is the reason why this framework was made and between its feature it is:

        1. Connect each model to the post_save signal for auto notifying users of changes in their requested fields.
        2. More coming soon...

        Each type base method should carefully handle the fields and resolve them, making a simple django model turn into a powerful GraphQL schema
        """
        logging.debug(f"{info}, {args}, {kwargs}")
        for i in range(5):
            yield cls(id=i, content=f"Ping #{i}")
            await asyncio.sleep(1)

    class Meta:
        abstract = True


def __channel_sync(sender: GQLModel, instance: GQLModel, **kwargs: dict[str, Any]):
    logging.debug("Syncing live channel after model update")


post_save.connect(__channel_sync, GQLModel, weak=False)
