"""
This submodule main goal is to handle the model definition interpretation to generate a graphql schema from it,
mostly this module is not about communication (e.g. socketio) but about the presentation layer (graphql).
"""
from .db_schema import GQLModel as Model
from . import fields
from .fields import (
    GQLField as Field,
    GQLURLField as URLField,
    GQLTextField as TextField,
    GQLManyToManyField as ManyToManyField,
    GQLForeignKey as ForeignKey,
    GQLDateField as DateField,
    GQLDateTimeField as DateTimeField,
    GQLUUIDField as UUIDField,
    GQLCharField as CharField,
)
from django.db.models import DO_NOTHING

__all__ = (
    "Model",
    "fields",
    "Field",
    "URLField",
    "TextField",
    "ManyToManyField",
    "ForeignKey",
    "DO_NOTHING",
    "DateField",
    "DateTimeField",
    "UUIDField",
    "CharField"
)
