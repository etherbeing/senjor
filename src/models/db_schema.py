from typing import cast, Any
from django.db import models
from django.apps import AppConfig
from graphene import ObjectType, Int
from senjor.graphql.core import graphql_schema
from graphene import String, Field
from .fields import GQLField, GQLAutoField


class GQLModelMeta(models.base.ModelBase):
    def __new__(cls, name, bases, attrs):
        instance: models.base.ModelBase = super().__new__(cls, name, bases, attrs)
        if not instance._meta.abstract:
            parent_ot = graphql_schema.add_node(
                instance.GQLObjectType, instance.__name__, instance
            )
            for (
                field_name,
                field_value,
            ) in (
                instance.__dict__.items()
            ):  # We calculated fields this way as django is yet not ready at this point, also we dont wait until is ready because it would make us iterate over all existent models which is slower
                if isinstance(
                    field_value,
                    (
                        models.fields.related_descriptors.ManyToManyDescriptor,
                        models.fields.related_descriptors.DeferredAttribute,
                        models.fields.related_descriptors.ForeignKeyDeferredAttribute,
                    ),
                ):
                    field: GQLField = instance._meta.get_field(field_name)
                    parent_ot.add_field(
                        field.name,
                        (
                            field.GQLObjectType()
                            if isinstance(field, GQLField)
                            else (
                                GQLAutoField.GQLObjectType()
                                if field.primary_key
                                else None
                            )
                        ),
                        field,
                    )
        return instance


class GQLModel(models.Model, metaclass=GQLModelMeta):
    """
    Define your GraphQL Schema and DB all in one, avoiding to repeat each field declaration here and in the graphql element
    """

    GQLObjectType = "query"

    class Meta:
        abstract = True
