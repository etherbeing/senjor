from django.conf import settings

## Setup dependency settings
settings.GRAPHENE = {
    "SCHEMA": "senjor.graphql.core.graphql_schema",
    "SCHEMA_INDENT": 2,
    "MIDDLEWARE": (),
    # Set to True if the connection fields must have
    # either the first or last argument
    "RELAY_CONNECTION_ENFORCE_FIRST_OR_LAST": False,
    # Max items returned in ConnectionFields / FilterConnectionFields
    "RELAY_CONNECTION_MAX_LIMIT": 100,
    "CAMELCASE_ERRORS": True,
    # Automatically convert Choice fields of Django into Enum fields
    "DJANGO_CHOICE_FIELD_ENUM_CONVERT": True,
    # Set to True to enable v2 naming convention for choice field Enum's
    "DJANGO_CHOICE_FIELD_ENUM_V2_NAMING": False,
    "DJANGO_CHOICE_FIELD_ENUM_CUSTOM_NAME": None,
    # Use a separate path for handling subscriptions.
    "SUBSCRIPTION_PATH": "/ws/graphql",
    # By default GraphiQL headers editor tab is enabled, set to False to hide it
    # This sets headerEditorEnabled GraphiQL option, for details go to
    # https://github.com/graphql/graphiql/tree/main/packages/graphiql#options
    "GRAPHIQL_HEADER_EDITOR_ENABLED": True,
    "GRAPHIQL_SHOULD_PERSIST_HEADERS": True,
    "GRAPHIQL_INPUT_VALUE_DEPRECATION": False,
    "ATOMIC_MUTATIONS": True,
    "TESTING_ENDPOINT": "/graphql",
    "MAX_VALIDATION_ERRORS": None,
}
