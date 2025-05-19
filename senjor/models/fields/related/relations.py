import logging
from typing import Any

from django.db.models.fields.reverse_related import ManyToManyRel as DjangoManyToManyRel
from django.db.models.fields.reverse_related import ManyToOneRel as DjangoManyToOneRel


class GQLManyToManyRel(DjangoManyToManyRel):
    def get_gql_field(self, *args: list[Any], **kwargs: dict[str, Any]):
        logging.debug(self.__dict__)


class GQLManyToOneRel(DjangoManyToOneRel):
    def get_gql_field(self, *args: list[Any], **kwargs: dict[str, Any]):
        logging.debug(self.__dict__)
