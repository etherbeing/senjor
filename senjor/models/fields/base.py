import logging
from typing import Any, Self, cast

import graphene
from django.conf import settings
from django.db.models import ForeignObjectRel as DjangoForeignObjectRel
from django.db.models import Model as DjangoModel
from django.db.models.fields import Field as DjangoField
from django.utils.module_loading import import_string
from graphene.types.base import BaseType

from senjor.core.exceptions import GQLBaseException
from senjor.models.fields.deferred import GQLDeferredAttribute
from senjor.models.fields.types import (  # Change the name so it doesnt got mistaken
    GQLSchemaType,
)


class GQLField(DjangoField):  # type: ignore[reportMissingTypeArgument]
    name: str
    model: DjangoModel
    # model: DjangoModel
    _gql_object_type: type[BaseType] = graphene.ObjectType
    _gql_field_value: graphene.Field | graphene.List | BaseType | None = None
    _gql_schema_type: GQLSchemaType = "general"
    descriptor_class = GQLDeferredAttribute

    # def __init__(
    #     self,
    #     *args: Any,
    #     **kwargs: Any,
    # ) -> None:
    #     super().__init__(*args, **kwargs)

    def __generate_gql_field(
        self, discard_related_from: DjangoModel | None = None
    ) -> None:
        """
        Generates the GraphQL field from this DB field
        """
        logging.debug(
            "Generating GraphQL field for the DB field %s...", self.get_gql_name()
        )
        model: DjangoModel | None = getattr(self, "model", None)
        if (
            model and not model._meta.abstract
        ):  # Dont generate schema types for abstract models
            kwargs: dict[str, Any] = {}
            kwargs["name"] = self.get_gql_name()
            kwargs["description"] = self.help_text or self.description or self.__doc__  # type: ignore
            if self._gql_schema_type in ["query", "general"]:
                if self.is_relation and (self.one_to_one or self.many_to_one):  # type: ignore
                    from senjor.models.base import GQLModel

                    # from senjor.models.fields.related.common import GQLRelatedField

                    fk_model: GQLModel | DjangoModel = self.related_model
                    if not issubclass(fk_model, GQLModel):  # type: ignore Solves by ID reference instead
                        # kwargs["name"] = f"{self.name}_{fk_model._meta.pk.get_attname()}" # type: ignore
                        self._gql_field_value = graphene.Field(
                            self.field_to_gql_field(
                                fk_model._meta.pk  # type: ignore
                            )._gql_object_type,
                            **kwargs,
                        )
                        logging.debug(
                            "Creating reference by PK to model %s and field %s",
                            fk_model,
                            self._gql_field_value,
                        )
                        logging.debug(
                            "Current model for FK created %s which have a relation with %s",
                            model,
                            fk_model,
                        )
                    else:  # Solves ObjectType until depth is reached
                        logging.debug(
                            "Found reference to ObjectType in model which is %s",
                            fk_model.get_gql_object_type().type,  # type: ignore
                        )
                        if not discard_related_from or fk_model is not cast(
                            type[GQLModel], discard_related_from
                        ):
                            self._gql_field_value = graphene.Field(
                                fk_model.get_gql_object_type().type, **kwargs  # type: ignore
                            )
                        else:
                            self._gql_field_value = (
                                self.field_to_gql_field(fk_model.pk)
                                .get_gql_field(self._gql_schema_type, fk_model)
                                .type(**kwargs)  # type: ignore
                            )
                elif self.is_relation and (self.many_to_many or self.one_to_many):  # type: ignore
                    # TODO Fix infinite recursion here
                    from senjor.models.base import GQLModel

                    # from senjor.models.fields.related.common import GQLRelatedField

                    fk_model: GQLModel | DjangoModel = self.related_model
                    if not issubclass(fk_model, GQLModel):  # type: ignore
                        raise GQLBaseException(
                            f"Field {self.get_gql_name()} points to {self.related_model} which doesn't inherit from {GQLModel.__name__} therefore we cannot generate the ObjectType require, if you want to ignore this field instead please pass gql_exclude to exclude this field from GQL"
                        )
                    if not discard_related_from or fk_model is not cast(
                        type[GQLModel], discard_related_from
                    ):
                        self._gql_field_value = graphene.List(
                            of_type=fk_model.get_gql_object_type(discard_related_from=model).type,  # type: ignore
                            **kwargs,
                        )
                    else:
                        self._gql_field_value = graphene.List(
                            self.field_to_gql_field(  # turns the Django Field into a GQL or Senjor Field
                                cast(DjangoField, fk_model._meta.pk)
                            )._gql_object_type,  # type: ignore Gets the GraphQL type to be used in a List or Field parent Type.
                            **kwargs,
                        )
                else:
                    logging.debug(
                        "Working on default gql object type %s", self._gql_object_type
                    )
                    logging.debug(
                        "Working on class %s and object of GQLField %s",
                        self.__class__.__name__,
                        self,
                    )
                    logging.debug(
                        "Class object type: %s", self.__class__._gql_object_type
                    )
                    self._gql_field_value = self._gql_object_type(**kwargs)

            logging.debug(
                "Created field with value: %s, and type: %s",
                self._gql_field_value,  # type: ignore
                self._gql_schema_type,
            )
        if not self._gql_field_value:  # type: ignore
            raise GQLBaseException(
                "Incorrect tree branch, we are missing a field to be generated possibly leading to inconsistent behavior, please report this at https://github.com/etherbeing/senjor/issues"
            )

    def get_gql_name(
        self,
    ) -> str:
        return self.name or getattr(self, "accessor_name", "")

    def get_gql_field(
        self,
        schema_type: GQLSchemaType,
        model_class: type[DjangoModel],
        discard_related_from: DjangoModel | None = None,
    ) -> graphene.Field:
        """
        Obtains the graphene Field for the given Schema, ready to be inserted into a ObjectType and be part of an Schema
        """
        self.__handle_hidden_field(model_class)
        if not self._gql_field_value:
            self._gql_schema_type = schema_type
            self.__generate_gql_field(discard_related_from=discard_related_from)
        logging.debug("Obtaining GQLField with value: %s", self._gql_field_value)
        return cast(graphene.Field, self._gql_field_value)

    def __handle_hidden_field(self, model_class: type[DjangoModel]):
        if getattr(self, "model", None) is None:
            if model_class._meta.auto_field.get_attname() == self.name:  # type: ignore
                model_class._meta.auto_field = None
            self.contribute_to_class(model_class, self.name)  # type: ignore

    def get_gql_object_type(self):
        return self._gql_object_type

    @classmethod
    def get_gql_from_field(
        cls, django_field: DjangoField | DjangoForeignObjectRel
    ) -> Self:
        kwargs: dict[str, Any] = {}
        if django_field.is_relation:  # type: ignore
            kwargs["to"] = django_field.model  # type: ignore
        gql_field = cls(**kwargs)
        logging.debug("Created a new object of type %s and value %s", cls, gql_field)
        logging.debug(
            "The new object created has an internal object type with value %s",
            gql_field._gql_object_type,
        )
        gql_field.__dict__.update(django_field.__dict__)
        return gql_field

    @classmethod
    def field_to_gql_field(cls, django_field: DjangoField) -> Self:
        """
        Returns the field used by senjor to represent the the django field
        """
        field_class_name = type(django_field).__name__
        gql_field: Self = import_string(f"senjor.models.{field_class_name}")
        return gql_field.get_gql_from_field(django_field)

    @classmethod
    def to_gql_field(
        cls,
        django_field: DjangoField | DjangoForeignObjectRel,
        schema_type: GQLSchemaType,
        model_class: type[DjangoModel],
        discard_related_from: DjangoModel | None = None,
    ) -> graphene.Field:
        """
        Convert GQLField object from a django field (model field) to a GraphQL field or graphene.Field
        """
        if isinstance(django_field, cls):
            return django_field.get_gql_field(
                schema_type=schema_type,
                model_class=model_class,
                discard_related_from=discard_related_from,
            )
        elif isinstance(django_field, DjangoForeignObjectRel):
            if django_field.is_relation:
                if django_field.many_to_many:  # type: ignore
                    from senjor.models.fields.related.common import GQLManyToManyField

                    field = GQLManyToManyField.get_gql_from_field(django_field)
                    field.__handle_hidden_field(model_class)
                    gql_field = field.get_gql_field(
                        schema_type,
                        model_class=model_class,
                        discard_related_from=discard_related_from,
                    )
                    return gql_field
                elif django_field.one_to_one:  # type: ignore
                    from senjor.models.fields.related.common import GQLForeignKey

                    field: DjangoField = GQLForeignKey.get_gql_from_field(django_field)
                    field.__handle_hidden_field(model_class)
                    field_gql = field.get_gql_field(
                        schema_type,
                        model_class=model_class,
                        discard_related_from=discard_related_from,
                    )
                    return field_gql
        elif isinstance(django_field, import_string(settings.DEFAULT_AUTO_FIELD)):
            return cls.field_to_gql_field(django_field).get_gql_field(
                schema_type=schema_type,
                model_class=model_class,
                discard_related_from=discard_related_from,
            )
        # if the function hasn't return so far then raise an error
        raise GQLBaseException(
            f"Unsupported field type, please fill a ticket on https://github.com/etherbeing/senjor/issues for this: Field Type {type(django_field)}, Field Repr: {django_field}"
        )
