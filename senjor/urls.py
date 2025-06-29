from django.urls import URLPattern, path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import AsyncGraphQLView

from senjor.core.attributes import graphql_schema

urlpatterns: list[URLPattern] = (
    [  # Defaults urls for the senjor ecosystem, the way is currently being used is to reduce user configurations
        path("graphql/", csrf_exempt(AsyncGraphQLView.as_view(schema=graphql_schema)))
    ]
)
