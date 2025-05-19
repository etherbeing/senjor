"""
This submodule main goal is to handle the model definition interpretation to generate a graphql schema from it,
mostly this module is not about communication (e.g. socketio) but about the presentation layer (graphql).
"""

from django.db.models import CASCADE, DO_NOTHING, SET_DEFAULT, SET_NULL

from senjor.models import fields
from senjor.models.base import GQLModel as Model
from senjor.models.fields import (
    AutoField,
    BigAutoField,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    Field,
    FloatField,
    IntegerField,
    TextField,
)
from senjor.models.fields.related.common import GQLForeignKey as ForeignKey
from senjor.models.fields.related.common import GQLManyToManyField as ManyToManyField

__all__ = (
    "fields",
    "TextField",
    "CharField",
    "ManyToManyField",
    "ForeignKey",
    "AutoField",
    "BigAutoField",
    "BooleanField",
    "DateField",
    "DateTimeField",
    "DecimalField",
    "EmailField",
    "Field",
    "FloatField",
    "IntegerField",
    "Model",
    "CASCADE",
    "SET_NULL",
    "SET_DEFAULT",
    "DO_NOTHING",
)
