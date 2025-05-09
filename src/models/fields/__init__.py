from django.db.models import ManyToManyField, ForeignKey
from django.db.models.fields import Field
from django.db.models import fields
import graphene
from typing import Optional, Callable, TypedDict
from enum import Enum
from senjor.graphql.core import graphql_schema
import logging


class AccessControl(Enum):
    PRIVATE: int = 0
    PUBLIC: int = 1
    PROTECTED: int = 2


class ActionType(TypedDict):
    mutation: Optional[Callable | str]
    subscription: Optional[Callable | str]
    query: Optional[Callable | str]


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

    GQLObjectType: graphene.ObjectType = graphene.ObjectType

    def __init__(
        self,
        *args,
        gql_access: Optional[AccessControl] = None,
        gql_action: ActionType = None,
        gql_is_argument: bool = False,
        **kwargs,
    ):
        """
        Create your graphql field like you create any other django model field

        :gql_access: Specify which one would be the scope of this field, if PROTECTED it will only be available if the user is authenticated, if PUBLIC it will always be available, and private won't be available
        :gql_action: Register the actions available for this field, like available under subscriptions, queries or mutations.
        """
        super().__init__(*args, **kwargs)


class GQLAutoField(fields.AutoField, GQLField):
    """
    This class is the default auto field once this is installed
    """

    GQLObjectType = graphene.BigInt


class GQLBigAutoField(fields.BigAutoField, GQLField):
    GQLObjectType = graphene.BigInt


class GQLForeignKey(ForeignKey, GQLField):
    GQLObjectType = graphene.ObjectType


class GQLManyToManyField(ManyToManyField, GQLField):
    GQLObjectType = graphene.ObjectType


class GQLURLField(fields.URLField, GQLField):
    GQLObjectType = graphene.String


class GQLTextField(fields.TextField, GQLField):
    GQLObjectType = graphene.String


class GQLDateField(fields.DateField, GQLField):
    GQLObjectType = graphene.Date


class GQLDateTimeField(fields.DateTimeField, GQLField):
    GQLObjectType = graphene.DateTime


class GQLUUIDField(fields.UUIDField, GQLField):
    GQLObjectType = graphene.UUID


class GQLCharField(fields.CharField, GQLField):
    GQLObjectType = graphene.String
