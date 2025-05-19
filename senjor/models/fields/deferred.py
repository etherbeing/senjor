import logging
from typing import Any

from django.db.models.fields.related_descriptors import (
    ForeignKeyDeferredAttribute as DjangoForeignKeyDeferredAttribute,  # type: ignore[reportAttributeAccessIssue]
)
from django.db.models.query_utils import DeferredAttribute


class GQLForeignKeyDeferredAttribute(DjangoForeignKeyDeferredAttribute):

    def get_gql_field(self, *args: list[Any], **kwargs: dict[str, Any]):
        logging.debug(self.__dict__)


class GQLDeferredAttribute(DeferredAttribute):

    def get_gql_field(self, *args: list[Any], **kwargs: dict[str, Any]):
        logging.debug(self.__dict__)
