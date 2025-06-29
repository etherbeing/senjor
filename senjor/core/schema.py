# GraphQL Schema autogeneration

import logging
from collections.abc import Callable, Iterator
from enum import Enum
from typing import Any, TypedDict

import strawberry
from django.apps import apps
from django.db.models import Model as DjangoModel

# from django.utils.translation import gettext as _
from strawberry.types.field import StrawberryField

from senjor.models.base import GQLModel


# types
class AccessControl(Enum):
    PRIVATE = 0
    PUBLIC = 1
    PROTECTED = 2


class ActionType(TypedDict):
    mutation: Callable[..., Any] | str | None
    subscription: Callable[..., Any] | str | None
    query: Callable[..., Any] | str | None


def generate_root_schema():
    logging.debug("Initializing schema...")
    gql_fields: dict[str, StrawberryField] = {}
    for app_config in apps.get_app_configs():
        logging.debug(f"Processing app {app_config}")
        models: Iterator[type[GQLModel] | type[DjangoModel]] = app_config.get_models()
        logging.debug(f"Senjor autodetected models are: {models}")
        for model in models:
            if issubclass(model, GQLModel):
                gql_fields[model.get_senjor_name()] = model.get_senjor_field()
    QueryType = strawberry.type(type("BaseQuery", (object,), gql_fields))
    MutationType = strawberry.type(type("MutationQuery", (object,), gql_fields))
    SubscriptionType = strawberry.type(type("SubscriptionQuery", (object,), gql_fields))

    return strawberry.Schema(
        query=QueryType, mutation=MutationType, subscription=SubscriptionType
    )
