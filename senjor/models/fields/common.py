import graphene
from django.db.models import fields as django_fields

from senjor.models.fields.base import (  # For internal usage only please use Field exported by senjor.models.fields instead
    GQLField,
)


class GQLAutoField(django_fields.AutoField, GQLField):  # type: ignore
    """
    This class is the default auto field once this is installed
    """

    _gql_object_type = graphene.Int


class GQLBigAutoField(django_fields.BigAutoField, GQLField):  # type: ignore
    _gql_object_type = graphene.BigInt


class GQLURLField(django_fields.URLField, GQLField):  # type: ignore[reportMissingTypeArgument]
    _gql_object_type = graphene.String


class GQLTextField(django_fields.TextField, GQLField):  # type: ignore[reportMissingTypeArgument]
    _gql_object_type = graphene.String


class GQLDateField(django_fields.DateField, GQLField):  # type: ignore[reportMissingTypeArgument]
    _gql_object_type = graphene.Date


class GQLDateTimeField(django_fields.DateTimeField, GQLField):  # type: ignore[reportMissingTypeArgument]
    _gql_object_type = graphene.DateTime


class GQLUUIDField(django_fields.UUIDField, GQLField):  # type: ignore[reportMissingTypeArgument]
    _gql_object_type = graphene.UUID


class GQLCharField(django_fields.CharField, GQLField):  # type: ignore[reportMissingTypeArgument]
    _gql_object_type = graphene.String


class GQLIntegerField(django_fields.IntegerField, GQLField):  # type: ignore[reportMissingTypeArgument]
    _gql_object_type = graphene.Int


class GQLBooleanField(django_fields.BooleanField, GQLField):  # type: ignore[reportMissingTypeArgument]
    _gql_object_type = graphene.Boolean


class GQLFloatField(django_fields.FloatField, GQLField):  # type: ignore[reportMissingTypeArgument]
    _gql_object_type = graphene.Float


class GQLDecimalField(django_fields.DecimalField, GQLField):  # type: ignore[reportMissingTypeArgument]
    _gql_object_type = graphene.Decimal


class GQLEmailField(django_fields.EmailField, GQLField):  # type: ignore[reportMissingTypeArgument]
    _gql_object_type = graphene.String
