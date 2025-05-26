from django.urls import URLPattern, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns: list[URLPattern] = (
    [  # Defaults urls for the senjor ecosystem, the way is currently being used is to reduce user configurations
        path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True)))
    ]
)
