from typing import Any

import strawberry
from django.db.models import ForeignKey as DjangoForeignKey
from django.db.models import ManyToManyField as DjangoManyToManyField
from django.db.models import manager as django_many_manager
from strawberry.types.base import StrawberryType

from senjor.models.base import GQLModel
from senjor.models.fields.base import (  # For internal usage only please use Field exported by senjor.models.fields instead
    GQLField,
)
from senjor.models.fields.deferred import (
    GQLDeferredAttribute,
    GQLForeignKeyDeferredAttribute,
)
from senjor.models.fields.related.relations import GQLManyToManyRel, GQLManyToOneRel


class GQLRelatedField(GQLField):
    _depth_state: dict[str, dict[str, dict[str, int]]] = {}

    def __init__(self, *args: Any, max_depth: int = 1, **kwargs: Any):
        # The recursion depth to look for tables, this is useful for avoid infinite recursion.
        self._max_depth = max_depth
        super().__init__(*args, **kwargs)

        self._instance_depth_state: dict[str, int] = {}

    def check(self, **kwargs: Any) -> dict[str, Any]:
        self._depth_state.get(  # type:ignore
            self.related_model._meta.app_label, {}
        ).get(
            self.related_model._meta.model_name
            or self.related_model.__class__.__name__,
            {self.get_senjor_name(): self._max_depth},
        )
        if self._instance_depth_state.get(self.get_senjor_name(), 0) > 0:
            self._instance_depth_state[self.get_senjor_name()] -= 1
            self._instance_depth_state[self.get_senjor_name()] -= 1

        return super().check(**kwargs)  # type: ignore


class GQLForeignKey(DjangoForeignKey, GQLRelatedField):  # type: ignore[reportMissingTypeArgument]

    descriptor_class = GQLForeignKeyDeferredAttribute
    rel_class = GQLManyToOneRel

    one_to_many: bool | None = DjangoForeignKey.one_to_many  # type: ignore[reportIncompatibleVariableOverride]
    one_to_one: bool | None = DjangoForeignKey.one_to_one  # type: ignore[reportIncompatibleVariableOverride]
    many_to_many: bool | None = DjangoForeignKey.many_to_many  # type: ignore[reportIncompatibleVariableOverride]
    many_to_one: bool | None = DjangoForeignKey.many_to_one  # type: ignore[reportIncompatibleVariableOverride]

    def resolve(self, info: strawberry.Info):
        if isinstance(self.related_model, GQLModel):  # type: ignore
            return strawberry.field(self.related_model.get_senjor_field())
        else:
            return GQLField.native_to_senjor_field(self.related_model._meta.pk).resolve(info)  # type: ignore


class GQLManyToManyField(DjangoManyToManyField, GQLRelatedField):  # type: ignore[reportMissingTypeArgument]

    descriptor_class = GQLDeferredAttribute
    rel_class = GQLManyToManyRel

    one_to_many: bool | None = DjangoManyToManyField.one_to_many  # type: ignore[reportIncompatibleVariableOverride]
    one_to_one: bool | None = DjangoManyToManyField.one_to_one  # type: ignore[reportIncompatibleVariableOverride]
    many_to_many: bool | None = DjangoManyToManyField.many_to_many  # type: ignore[reportIncompatibleVariableOverride]
    many_to_one: bool | None = DjangoManyToManyField.many_to_one  # type: ignore[reportIncompatibleVariableOverride]

    async def resolve(self, info: strawberry.Info):
        m2m_related: django_many_manager.ManyToManyRelatedManager[Any, Any] = (
            self.get_value(info)
        )
        return_type = self.resolve.__annotations__.get("return")
        elements: list[GQLModel | Any] = []
        is_nested_model = issubclass(
            getattr(return_type, "__args__", [None])[0], StrawberryType
        )

        async for element in m2m_related.all():
            elements.append((element if is_nested_model else element.pk))
        return elements
