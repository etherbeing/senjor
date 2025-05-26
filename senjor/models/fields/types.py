from typing import Literal, TypedDict

from django.db.models import Model as DjangoModel

type GQLSchemaType = Literal["query", "mutation", "subscription"]

class FieldStruct(TypedDict):
    query: dict[str, type[DjangoModel]]
    mutation: dict[str, type[DjangoModel]]
    subscription: dict[str, type[DjangoModel]]