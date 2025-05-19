from typing import Literal, TypedDict

from django.db.models import Model as DjangoModel

type GQLSchemaType = Literal["query", "mutation", "subscription", "general"]

class FieldStruct(TypedDict):
    query: dict[str, type[DjangoModel]]
    mutation: dict[str, type[DjangoModel]]
    subscription: dict[str, type[DjangoModel]]
    general: dict[str, type[DjangoModel]]