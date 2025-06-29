import datetime
import decimal

import strawberry
from django.db.models import fields as django_fields
from strawberry.schema.types.base_scalars import UUID  # , Date, DateTime

from senjor.models.fields.base import (  # For internal usage only please use Field exported by senjor.models.fields instead
    GQLField,
)


class GQLAutoField(django_fields.AutoField, GQLField):  # type: ignore
    """
    This class is the default auto field once this is installed
    """

    def resolve(self, info: strawberry.Info) -> int:
        return self.get_value(info)  # type: ignore


class GQLBigAutoField(django_fields.BigAutoField, GQLField):  # type: ignore
    def resolve(self, info: strawberry.Info) -> int:
        return self.get_value(info)


class GQLURLField(django_fields.URLField, GQLField):  # type: ignore[reportMissingTypeArgument]
    def resolve(self, info: strawberry.Info) -> str:
        return self.get_value(info)


class GQLTextField(django_fields.TextField, GQLField):  # type: ignore[reportMissingTypeArgument]
    def resolve(self, info: strawberry.Info) -> str:
        return self.get_value(info)


class GQLDateField(django_fields.DateField, GQLField):  # type: ignore[reportMissingTypeArgument]
    def resolve(self, info: strawberry.Info) -> datetime.date:
        return self.get_value(info)


class GQLDateTimeField(django_fields.DateTimeField, GQLField):  # type: ignore[reportMissingTypeArgument]
    def resolve(self, info: strawberry.Info) -> datetime.datetime:
        return self.get_value(info)


class GQLUUIDField(django_fields.UUIDField, GQLField):  # type: ignore[reportMissingTypeArgument]
    def resolve(self, info: strawberry.Info) -> UUID:  # type: ignore
        return self.get_value(info)


class GQLCharField(django_fields.CharField, GQLField):  # type: ignore[reportMissingTypeArgument]
    def resolve(
        self,
        info: strawberry.Info,
    ) -> str:
        return self.get_value(info)


class GQLIntegerField(django_fields.IntegerField, GQLField):  # type: ignore[reportMissingTypeArgument]
    def resolve(self, info: strawberry.Info) -> int:
        return self.get_value(info)


class GQLBooleanField(django_fields.BooleanField, GQLField):  # type: ignore[reportMissingTypeArgument]
    def resolve(self, info: strawberry.Info) -> bool:
        return self.get_value(info)


class GQLFloatField(django_fields.FloatField, GQLField):  # type: ignore[reportMissingTypeArgument]
    def resolve(self, info: strawberry.Info) -> float:
        return self.get_value(info)


class GQLDecimalField(django_fields.DecimalField, GQLField):  # type: ignore[reportMissingTypeArgument]
    def resolve(self, info: strawberry.Info) -> decimal.Decimal:
        return self.get_value(info)


class GQLEmailField(django_fields.EmailField, GQLField):  # type: ignore[reportMissingTypeArgument]
    def resolve(self, info: strawberry.Info) -> str:
        return self.get_value(info)
