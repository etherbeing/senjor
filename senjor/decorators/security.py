"""
Handles authentication on graphql over socket.io endpoints
"""

from typing import Optional
from graphql import GraphQLError


def op_protected(scope: Optional[str]=None):
    """
    Operation protected decorator to protect a graphql operation (Query, Mutation, Subscription) with authentication
    Decorator to protect a graphql field (ObjectType) with authentication
    usage:
    ```python
    class Query(ObjectType):
        hello = String()

        @protected
        def resolve_hello(self, info):
            return "Hello world"
    ```
    """
    def decorator(func):
        def wrapper(info, *args, **kwargs):
            # Check if the user is authenticated
            if not info.user.is_authenticated:
                raise GraphQLError("Authentication required")
            return func(*args, **kwargs)
        return wrapper
    return decorator