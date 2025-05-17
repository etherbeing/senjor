"""
In this file is handled the main parts of the schema generation from models
TODO: please REFACTOR this file to be more readable, APIs must follow a tight scoped separation per file
"""
import json
import logging
from enum import Enum
from collections.abc import Callable
from typing import Self
from typing import Any
from typing import TypedDict, Literal

import graphene
from django.db import models
from django.db.models import ManyToManyField, ForeignKey
from django.db.models import fields
from graphql import GraphQLResolveInfo


# types

class AccessControl(Enum):
    PRIVATE = 0
    PUBLIC = 1
    PROTECTED = 2


class ActionType(TypedDict):
    mutation: Callable[..., Any] | str | None
    subscription: Callable[..., Any] | str | None
    query: Callable[..., Any] | str | None


type GQLSchemaType = Literal["query", "mutation", "subscription", "general"]


# end types

# GQL Object Type schema
class GQLObjectType:

    def __init__(self, name: str, operation_type: GQLSchemaType, parent:Self|None=None, model_class: type[models.Model]|None = None):
        self._name: str = name
        self._model_class: type[models.Model]|None = model_class
        self._registered: bool = False
        self._operation_type: GQLSchemaType = operation_type
        from senjor.core.attributes import graphql_schema
        self._parent: GQLRootSchema|Any = parent or graphql_schema
        self._fields: set[GQLField] = set()
        self._args: dict[str, graphene.Argument] = {}

    @property
    def name(self) -> str:
        return self._name

    def get_args(self, ):
        return self._args

    def add_field(self, field):
        """
        Add a field to this ObjectType, stack it so you can nest ObjectTypes like below
        ```py
        GQLObjectType().add_field("my_field").add_field("my_children")
        ```
        The above give us:
        ```graphql
        query Object{
            my_field {
                my_children
            }
        }
        ```
        """
        self._fields.add(field)
        self._args.update({field.name: graphene.Argument(field.gql_object_type, name=field.name, required=False)})
        if not self._registered:
            self._parent.add_field(self._operation_type, self)
            self._registered = True
        return self

    def get_value(self, ) -> graphene.ObjectType:
        fields: dict[str, graphene.Field] = {}
        for field in self._fields:
            fields[field.name] = field.get_value()
        # NOTE: Queries always use graphene.Field
        ot_result = graphene.Field(
            type(self._name, (graphene.ObjectType,), fields),
            description=self._model_class.__doc__,
            resolver=self._default_resolver,
            name=self._name,
            args=self.get_args(),
        )
        logging.debug("%s %s", ot_result.__dict__, fields)
        return ot_result

    def _default_resolver(self, root:Any, info: GraphQLResolveInfo, *args:list[Any], **kwargs: dict[str, Any]):
        logging.debug(args)
        logging.debug(kwargs)
        logging.debug(info.context.__dict__)
        logging.debug(info)
        # model_instance: models.Model
        model_rows: models.QuerySet = self._model_class.objects.filter(**kwargs)
        logging.debug(self.get_args().keys())
        if model_rows.count() > 1:
            rows = []
            for row in model_rows:
                keys = self.get_args().keys()
                args = dict(filter(lambda item: item[0] in keys, row.__dict__.items()))
                logging.debug(args)
                rows.append(self.get_value()._type(
                    **args
                ))
            return rows
        else:
            result: models.Model = model_rows.first()  # use a serializer like the one from DRF for now lets just do the next
            keys = self.get_args().keys()
            args = dict(filter(lambda item: item[0] in keys, result.__dict__.items()))
            logging.debug(args)
            return self.get_value()._type(
                **args
            )

    def __repr__(
            self,
    ):
        return self.__str__()

    def __str__(self):
        return f"{self.__class__.__name__}:{self._name}:{self._fields}"


# Fields management
class GQLField(fields.Field):
    """
    # GQLField

    Enable the capabilities of GQL to work over socket.io under the hood, just plug and play
    NOTE: To install your model as a GraphQL Schema just replace the code as follows:

    ## Quickstart (Full migration)

    ```py
    # from django.db import models
    from gql_socketio import models
    ```

    The above is all you need, our api is fully compatible with django default models and fields

    ## Full Usage Example (Taken from a functional project)
    ```py
    from django.contrib.auth import get_user_model
    from gql_socketio import models

    User = get_user_model()

    class MessageAttachment(models.Model):
        s3_file_link = models.URLField(verbose_name=_("File Link"), help_text=_("The link of the file to be attached to a message"))


    class ChatMessage(models.Model):
        message = models.TextField(
            help_text=_(
                "The message to be sent to the user (can be optional to just send attachments (either message or attachments must be not null))"
            ), null=True, blank=True,
            verbose_name=_("Message")
        )
        attachments = models.ManyToManyField(
            MessageAttachment,
            verbose_name=_("Attachments"),
            help_text=_("The files or attachments for this message"),
            blank=True
        )
        sender = models.ForeignKey(
            User, on_delete=models.DO_NOTHING, verbose_name=_("Sender"),
            related_name="chat_sent",
            help_text=_("The sender user")
        )
        created_at = models.DateTimeField(auto_created=True, help_text="Creation time of the message")

    class CommunicationChannel(models.Model):
        id = models.UUIDField(default=uuid4, primary_key=True, unique=True, auto_created=True, editable=False)
        messages = models.ManyToManyField(ChatMessage)
        created_at = models.DateTimeField(auto_created=True, help_text="Creation time of the communication channel")
    ```

    We don't do any effort yet to expose a normalized api, so we expose the same names you use in your class definition, but please note that graphene by default does normalize your input, so we are going to be using graphene normal behaviour below.
    ## Generated GraphQL schema

    ```graphql
    query ChatQuery {
        MessageAttachment{
            s3FileLink
        }
        ChatMessage{
            message,
            attachments{
                s3FileLink
            },
            sender{
                username
            },
            createdAt
        }
        CommunicationChannel{
            id,
            messages,
            createdAt
        }
    }
    ```

    Similars subscriptions and mutation are made for the same object types described above, default arguments for each one of the object types are:

    1. id: Allows to filter an specific model by its id.

    By using the parameter is_argument, you turn the field into an argument for its ObjectType definition.
    """

    gql_object_type: type[graphene.ObjectType] = graphene.String
    gql_ref_type: type[graphene.ObjectType]|None = None
    gql_value: graphene.Field = None
    gql_name: str

    def __init__(
            self,
            gql_access: AccessControl|None = None,
            gql_action: ActionType = None,
            gql_is_argument: bool = False,
            *args,
            **kwargs,
    ):
        """
        Create your graphql field like you create any other django model field

        :gql_access: Specify which one would be the scope of this field, if PROTECTED it will only be available if the user is authenticated, if PUBLIC it will always be available, and private won't be available
        :gql_action: Register the actions available for this field, like available under subscriptions, queries or mutations.
        """
        super().__init__(*args, **kwargs)

    def populate(self):
        if not self.model._meta.abstract:
            kwargs: dict[str, Any] = {}
            self.gql_name = self.name
            if self.gql_ref_type:
                kwargs["of_type"] = self.gql_ref_type
            kwargs["name"] = self.gql_name
            kwargs['description'] = self.__doc__
            if self.model._gql_operation_type == "query":
                self.gql_value = graphene.Field(self.gql_object_type, **kwargs)
            logging.debug(f"%s %s", self.gql_value, self.model._gql_operation_type)
            self.model._gql_object_type.add_field(
                self)  # in case is already there the set nature of the add_field function ignores the field

    def check(self, **kwargs):
        """
        On field checking handle the auto install of this field in the graphql schema
        """
        self.populate()
        return super().check(**kwargs)

    def get_value(self, ) -> graphene.Field:
        if not self.gql_value:
            self.populate()
        return self.gql_value

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return f"{self.__class__.__name__}:{self.model._meta.model_name}:{self.gql_name}"

    def __repr__(self):
        return self.__str__()


class GQLAutoField(fields.AutoField, GQLField):
    """
    This class is the default auto field once this is installed
    """

    gql_object_type = graphene.ID


class GQLBigAutoField(fields.BigAutoField, GQLField):
    gql_object_type = graphene.ID


class GQLForeignKey(ForeignKey, GQLField):
    gql_object_type = graphene.String


class GQLManyToManyField(ManyToManyField, GQLField):
    gql_object_type = graphene.String


class GQLURLField(fields.URLField, GQLField):
    gql_object_type = graphene.String


class GQLTextField(fields.TextField, GQLField):
    gql_object_type = graphene.String


class GQLDateField(fields.DateField, GQLField):
    gql_object_type = graphene.Date


class GQLDateTimeField(fields.DateTimeField, GQLField):
    gql_object_type = graphene.DateTime


class GQLUUIDField(fields.UUIDField, GQLField):
    gql_object_type = graphene.UUID


class GQLCharField(fields.CharField, GQLField):
    gql_object_type = graphene.String


# Models managements
class GQLModelMeta(models.base.ModelBase):
    def __new__(cls, name, bases, attrs):
        instance: models.base.ModelBase = super().__new__(cls, name, bases, attrs)
        return instance


class GQLModel(models.Model, metaclass=GQLModelMeta):
    """
    Define your GraphQL Schema and DB all in one, avoiding repeating each field declaration here and in the graphql element
    """
    _gql_object_type: GQLObjectType = None
    _gql_operation_type = "query"
    _gql_fields: set[GQLField] = set()

    @classmethod
    def check(cls, **kwargs):
        cls._gql_object_type = cls._get_gql_field()
        return super().check()

    @classmethod
    def _get_gql_field(cls):
        if cls._gql_object_type is None:
            cls._gql_object_type = GQLObjectType(
                cls._meta.model_name,
                cls._gql_operation_type,
                model_class=cls
            )
        return cls._gql_object_type

    class Meta:
        abstract = True


class FieldStruct(TypedDict):
    query: set[GQLObjectType]
    mutation: set[GQLObjectType]
    subscription: set[GQLObjectType]
    general: set[GQLObjectType]


# Root Object Types management
class GQLRootSchema:
    """
    Handles the root object types meaning a singleton instance for Query, Mutation, Subscription. All others ObjectTypes must inherit from GQLObjectType instead.

    """
    _fields: FieldStruct = {
        "query": set(),
        "mutation": set(),
        "subscription": set(),
        "general": set(),
    }

    def __init__(
            self,
    ) -> None:
        self._model_instance: models.Model
        self._pending_object_types: dict[str, GQLObjectType] = {}

    def model_to_schema(
            self, model: models.Model, operation_type: GQLSchemaType = "query"
    ) -> graphene.ObjectType|None:
        return self._fields.get(operation_type, {}).get(
            model._meta.object_name, None  # type: ignore
        )

    def add_field(
            self,
            gql_type: GQLSchemaType,
            gql_field: GQLObjectType,
    ) -> GQLObjectType:
        """
        Add a GQL field to one of the base ObjectTypes (either query,mutation or subscription)
        """
        self._fields[gql_type].add(gql_field)
        return gql_field

    def add_query_field(
            self, gql_field: GQLObjectType
    ) -> GQLObjectType:
        return self.add_field("query", gql_field)

    def add_mutation_field(
            self, gql_field: GQLObjectType
    ) -> GQLObjectType:
        return self.add_field("mutation", gql_field)

    def add_subscription_field(
            self, gql_field: GQLObjectType
    ) -> GQLObjectType:
        return self.add_field("subscription", gql_field)

    def get_value(self, gql_type: GQLSchemaType) -> type(graphene.ObjectType):
        _fields: set[GQLObjectType] = (
            self._fields[gql_type].union(self._fields["general"])
        )
        fields: dict[str, graphene.ObjectType | graphene.Mutation] = {}
        for field in _fields:
            fields[field.name] = field.get_value()
        # logging.debug(type(f"Base{gql_type.title()}", (graphene.ObjectType,), fields).message.__dict__)
        return type(f"Base{gql_type.title()}", (graphene.ObjectType,), fields)

    def generate_query_type(
            self,
    ) -> graphene.ObjectType:
        return self.get_value("query")

    def generate_mutation_type(
            self,
    ) -> graphene.ObjectType:
        return self.get_value("mutation")

    def generate_subscription_type(
            self,
    ) -> graphene.ObjectType:
        return self.get_value("subscription")

    @property
    def value(
            self,
    ):
        logging.info("Debugging Fields: %s", json.dumps(self._fields, default=lambda o: str(o), indent=4))
        return graphene.Schema(
            query=(
                self.generate_query_type()
                if len(self._fields["query"].union(self._fields["general"])) > 0
                else None
            ),
            mutation=(
                self.generate_mutation_type()
                if len(self._fields["mutation"].union(self._fields["general"])) > 0
                else None
            ),
            subscription=(
                self.generate_subscription_type()
                if len(self._fields["subscription"].union(self._fields["general"])) > 0
                else None
            ),
        )

    def __getattribute__(self, name: str):
        try:
            value = super().__getattribute__(name)
        except AttributeError:
            value = super().__getattribute__("value")
            value = value.__getattribute__(name)
        return value

    __class__ = graphene.Schema  # Make Graphene to think this is a graphene.Schema

    def __dict__(
            self,
    ):
        return self._fields

    def __repr__(
            self,
    ):
        return str(self._fields)
