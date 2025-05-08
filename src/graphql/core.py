import logging
import graphene
from typing import Any, TypedDict, Type, Literal, Self, Optional
from django.db import models

type GQLSchemaType = Literal["query", "mutation", "subscription", "general"]


class GQLObjectType:

    def __init__(self, name: str = None):
        self._name = name
        self._fields: dict[str, GQLObjectType] = {}
        self._model_field: GQLObjectType
        self._pending_fields: list[dict[str, Any]] = []

    def add_field(self, name: str, value: Self, model_field: Self):
        """
        Add a field to this ObjectType, stack it so you can nest ObjectTypes like below
        ```py
        GQLObjectType().add_field("my_field").add_field("my_children")
        ```
        The above give us:
        ```graphql
        query Object{
            my_field {
                my_children
            }
        }
        ```
        """
        self._fields[name] = value
        self._model_field = model_field
        return self
    
    def add_pending_field(self, name: str, value: Self, *args, model_field: models.Field, model_instance: models.Model, **kwargs,):
        """
        Schedule a field to be added to the schema
        """
        self._pending_fields.append({
            "name": name,
            "value": value,
            "args": args,
            "kwargs": kwargs,
            "field": model_field,
            "model": model_instance
        })
        graphql_schema.add_pending_object_type(self)
        return self
    
    def complete(self,):
        for field in self._pending_fields:
            field_: models.ManyToManyField = field.get("field")
            object_type = graphql_schema.model_to_schema(field_.related_model)
            print(graphql_schema._fields, object_type, field_.related_model._meta.object_name)

    def generate_type(
        self,
    ) -> graphene.ObjectType:
        fields: dict[str, graphene.ObjectType] = {}
        # Handle dynamic field generations on the ObjectType
        for field_name, field_value in self._fields.items():
            logging.info("%s, %s: %s", self._name, field_name, field_value)
            if isinstance(field_value, GQLObjectType):
                fields[field_name] = field_value.generate_type()
            else:
                fields[field_name] = field_value
        object_type: graphene.ObjectType = type(
            self._name, (graphene.ObjectType,), fields
        )
        return object_type


class FieldStruct(TypedDict):
    query: list[GQLObjectType]
    mutation: list[GQLObjectType]
    subscription: list[GQLObjectType]
    general: list[GQLObjectType]


class GQLRootSchema:
    _fields: FieldStruct = {
        "query": {},
        "mutation": {},
        "subscription": {},
        "general": {},
    }

    def __init__(
        self,
    ):
        self._model_instance: models.Model
        self._pending_object_types: dict[str, GQLObjectType] = {}

    def model_to_schema(
        self, model: models.Model, operation_type: GQLSchemaType = "query"
    ) -> Optional[graphene.ObjectType]:
        return self._fields.get(operation_type, {}).get(
            model._meta.object_name, None # type: ignore
        )
    
    def add_pending_object_type(
        self, object_type: GQLObjectType
    ):
        self._pending_object_types[object_type._name] = object_type
        return self

    def add_field(
        self,
        gql_type: GQLSchemaType,
        name: str,
        gql_field: GQLObjectType,
        model_instance: models.Model,
    ) -> GQLObjectType:
        """
        Add a GQL field to one of the base ObjectTypes (either query,mutation or subscription)
        """
        self._fields[gql_type][name] = gql_field
        self._model_instance = model_instance
        return gql_field
        

    def add_node(
        self, gql_type: GQLSchemaType, name: str, model_instance: models.Model
    ) -> GQLObjectType:
        """
        Add a node to the root ObjectType, think of a node like a nested ObjectType inside another one.
        """
        return self.add_field(gql_type, name, GQLObjectType(name), model_instance)

    def add_query_field(
        self, name: str, gql_field: graphene.ObjectType, model_instance: models.Model
    ) -> GQLObjectType:
        return self.add_field("query", name, gql_field, model_instance)

    def add_mutation_field(
        self, name: str, gql_field: graphene.ObjectType, model_instance: models.Model
    ) -> GQLObjectType:
        return self.add_field("mutation", name, gql_field, model_instance)

    def add_subscription_field(
        self, name: str, gql_field: graphene.ObjectType, model_instance: models.Model
    ) -> GQLObjectType:
        return self.add_field("subscription", name, gql_field, model_instance)

    def generate_type(self, gql_type: GQLSchemaType) -> graphene.ObjectType:
        _fields: dict[str, GQLObjectType] = (
            self._fields[gql_type] | self._fields["general"]
        )
        fields: dict[str, graphene.ObjectType | graphene.Mutation] = {}
        for field_key, field_value in _fields.items():
            if isinstance(field_value, GQLObjectType):
                fields[field_key.lower()] = field_value.generate_type()
            else:
                # if isinstance(field_value, graphene.ObjectType):
                #     fields[field_key.lower()] = graphene.Field(field_value)
                # else:
                fields[field_key.lower()] = field_value
            field = fields[field_key.lower()]
            if gql_type == "query" or gql_type == "general":
                fields[field_key.lower()] = graphene.Field(
                    field,
                )
            elif gql_type == "mutation" or gql_type == "general":
                fields[field_key.lower()] = field.Field()
            elif gql_type == "subscription" or gql_type == "general":
                fields[field_key.lower()] = graphene.Field(
                    field,
                )
        for object_type in self._pending_object_types.values():
            object_type.complete()
        return type(f"Base{gql_type.title()}", (graphene.ObjectType,), fields)

    def generate_query_type(
        self,
    ) -> graphene.ObjectType:
        return self.generate_type("query")

    def generate_mutation_type(
        self,
    ) -> graphene.ObjectType:
        return self.generate_type("mutation")

    def generate_subscription_type(
        self,
    ) -> graphene.ObjectType:
        return self.generate_type("subscription")

    @property
    def value(
        self,
    ):
        return graphene.Schema(
            query=(
                self.generate_query_type()
                if len(self._fields["query"] | self._fields["general"]) > 0
                else None
            ),
            mutation=(
                self.generate_mutation_type()
                if len(self._fields["mutation"] | self._fields["general"]) > 0
                else None
            ),
            subscription=(
                self.generate_subscription_type()
                if len(self._fields["subscription"] | self._fields["general"]) > 0
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

    __class__ = graphene.Schema  # Make Graphene to think this is a graphene.Schema

    def __dict__(
        self,
    ):
        return self._fields


# Root Schema definition
graphql_schema = GQLRootSchema()
