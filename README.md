# Senjor
This django app allows you to integrate quickly and easily your project with the RTC tech socket.io, it quickly allows you to send GraphQL queries over socket.io as easy as you would declarate any other endpoint for DRF. Furthermore we provides you with some out of the box features to integrates with oauth as your security provider (this is tested against Keycloak containers and we fully officialy support just Keycloak Containers as the oauth providers). Feel free to PR any new feature you may feel like adding.

## Installation
```sh
pip install senjor
```

## Post-Install Steps
```python
# settings.py
INSTALLED_APPS=[
  ...,
  "senjor",
  ...
]
#asgi.py
"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from senjor import setup_sio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourprojectname.settings')


application = setup_sio(get_asgi_application())
```

## Idea
The idea of this project is simplify the creation of graphql queries over an live connection or real time connection as much as possible, I think the best way of doing this is by merging the Django native models and the graphql schema declaration, something like the models declared in django model are by default models exposed on the graphql schema, using decorators like @private to protect a model field from being exposed and @protected to allow the field to only be exposed after authenticate the request. Yet we have another 3 business to take care of, 1st: GraphQL Queries, 2nd: GraphQL Mutations and last but not least 3rd: GraphQL Subscriptions, each one of those operations can be summarized as by default simple CRUD, each model field could share a default operation, the decorators @private, @protected and @public could receive an integer (from an enum like class and | for reducing all options) that represent where the field is private by default is 1|2|3, which mean QUERY|MUTATION|SUBSCRIPTION=1 or could also be any other binary op, the api could just get a number predetermined by the enum.

For overriding the resolver for the field we could make the decorator receive a string or a callable pointing to the resolver, this would be using kwargs like:
```py
class MyModel(gql.GQLModel){
  @public(
    subscribe="my_subscribe_resolver"
  )
  my_field = gql.Char()
}
```
The above is not possible in python though it would be cool as hell to have that available in python T_T.

Another possibility would be overriding the Django fields so each field allow new params and allow to register the GQL schema in place something like:
```py
class MyModel(gql.GQLModel){
  my_field = gql.Char(
    verbose_name="My Django normal verbose name",
    gql_subscribe="my_subscribe_resolver", gql_public=True
    )
}
```

Which one is more pythonic? I think the second, now the problem with conventions, separation of concerns, the model does a lot of things now in django, and should only care about the db part and not the business logic (I know some terrible people in some other frameworks says the model should care about the logic as well and because of that the code is hard as hell to maintain [psd: Not talking about you Odoo devs :-)]).
Then for separation of concerns we can expand the later logic to include a file dedicated to the schemas logic, this file could be configured by using a var in the model named gql_subscription_class, gql_mutation_class, gql_query_class. The classes will only contain the resolvers using the notation: `<resolver_type>_field_name` where the resolver_type is either, mutation, query, subscription. By default the 3 configurations vars in the model are None, and the gql_socketio will look for a file named schema.py in the root of the app or a folder, depending on whether the model is within a folder or on the app root as a file, if the file is not found then it defaults to the default behaviour.

### Security
There should be a settings to configure senjor as default public or default private, also to define the default authentication framework for all queries, initially we are just going to implement the oauth auth mechanism that integrates well with Keycloak server

## TODO
1. Implement the Arguments for the queries
2. Implement the Mutations
3. Implement the subscriptions
4. Implement the resolvers
5. Implement the customization and the uniform API

## 

That’s a solid starting point. You're already close to building something extremely valuable to the community. What you’re aiming to do—**a plug-and-play authentication wrapper for GraphQL queries, mutations, and subscriptions in Django using OAuth2**—**does not yet exist in a clean, reusable form**, and it's **in high demand**.

Let’s break down exactly what your library should include and how it should be structured if you want it to gain wide adoption.

---

## **Minimum Viable Features (v0.1)**
To be used and loved by the community, your lib needs:

### **1. Decorator-Based Authorization for GraphQL Resolvers**
- Decorator like `@require_oauth(scope="read:users")` for:
  - Queries
  - Mutations
  - Subscriptions
- Internally validates token from context (`info.context` or request) using pluggable backends.

### **2. Pluggable Authentication Backends**
Allow this via config:
```python
GRAPHQL_OAUTH = {
    "AUTH_BACKEND": "myproject.auth.verify_token",
    "SCOPES_ENABLED": True
}
```
- Backend function receives token or context and returns:
  ```python
  {
      "active": True,
      "user": User object or dict,
      "scopes": ["read:users", ...]
  }
  ```
- Abstracts whether it's Django OAuth Toolkit, Auth0, Firebase, etc.

### **3. Graceful Fallback / Error Raising**
- Raise `GraphQLError("Unauthorized")` or return a custom 401 JSON.
- Optional: provide a middleware that auto-adds user info to context.

---

## **Bonus Features (v0.2+)**
Add these and your lib becomes the go-to standard:

### **4. GraphQL Subscription Auth (via WebSocket headers or `connectionParams`)**
- Validate access tokens on WebSocket handshake.
- Reject unauthorized connections.
- Bonus: Integrate with `channels_graphql_ws` or `strawberry.subscriptions`.

### **5. Prebuilt Backends for Popular Providers**
- `from graphql_oauth.backends import DOTBackend, Auth0Backend`
- Helps newcomers bootstrap quickly.

### **6. Integration with Django Permissions/Groups**
- Optional integration with Django’s permission system.
- Let users write something like `@require_perm("auth.change_user")`.

---

## **Code Quality & Ecosystem Standards**

### **Project Structure**
```plaintext
graphql_oauth/
  __init__.py
  decorators.py      <- @require_oauth
  exceptions.py
  backends/
    __init__.py
    base.py
    dot.py           <- Django OAuth Toolkit
    auth0.py         <- Auth0 example
  utils.py
  middleware.py      <- Optional: adds `request.user` if valid
  settings.py
tests/
docs/
setup.py
README.md
```

### **Dev Practices**
- Typed code (`mypy`-friendly).
- 100% test coverage with `pytest` and `pytest-django`.
- Supports Django 3.2 – 5.x.
- Python 3.9+ at least.

---

## **Marketing & Adoption**
Here’s how you make it **popular**:

- Name: Something clean and obvious, like `graphql-oauth-django` or `django-graphql-oauth`.
- Use `graphene` as a dependency, not a reimplementation.
- Write a blog post and publish on Medium/Dev.to: “Secure GraphQL Queries in Django with One Decorator”
- Example repo/demo app in the README.
- Package on PyPI.

---

## TL;DR: Must-Have Features

| Feature                              | Required for MVP? | Why? |
|--------------------------------------|-------------------|------|
| `@require_oauth()` decorator         | Yes               | Easy dev experience |
| Pluggable token verification backend | Yes               | Flexibility |
| Config-based setup                   | Yes               | Simplicity |
| GraphQL context integration          | Yes               | Access to token/user |
| WS connection param auth             | MVP+              | Required for subs |
| Subscription auth on connect        | MVP+              | Completes feature set |
| Django permission tie-in             | Optional          | Wider use cases |
| Strong test suite                    | Yes               | Trust & adoption |
