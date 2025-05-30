# Senjor

This django app allows you to integrate quickly and easily your project with the RTC tech socket.io, it quickly allows you to send GraphQL queries over socket.io as easy as you would declare any other endpoint for DRF. Furthermore we provides you with some out of the box features to integrates with oauth as your security provider (this is tested against Keycloak containers and we fully officialy support just Keycloak Containers as the oauth providers). Feel free to PR any new feature you may feel like adding.

## Installation

```sh
pip install senjor # bare pip
poetry add senjor # poetry install
uv install senjor # uv install
pipenv install senjor # pipenv install
```

## Post-Install Steps

```python
# demo.py
INSTALLED_APPS=[
  ...,
  "senjor",
  ...
]
```

## The idea behind Senjor

Senjor came after I by second time had to work on an RTC project for a Social Network, and I noticed that the setup was exactly like before, first install
django-channels, then configure the ASGI server (daphne in my case), then configure websocket, but as websocket consumers by default at least as I see it are
too messy and we need to handle the connect event and other stuff I did search for something different, perhaps not better but at least different, and this was
socket.io, then when searching for an already integrated tool for socket.io and django... well there was none, so I decided to create my own on top of those
before-mentioned tools, problems arise and this is very important as of today 29/5/2025 Django doesn't fully support ASGI servers, I mean the most exciting part
of django, at least how I see it its ORM is not fully asynchronous, but that want bring me down, Senjor will continuously work on:

1. Bringing to you the best Web Framework ever created until the date, making it out-of-the-box compatible with ASGI clients.
2. Giving you a powerful tool to create APIs like never before, close enough to a Real Time RPC, but without the hassle of worrying about the security.
3. Bringing OAuth and its scopes to you, so from a server like Keycloak (the one we are gonna test it against) you can define which fields and models a user can access.
4. You want to extend it? Ok no problem but do it easily no need for serializing yourself for cleaning the fields and stuff like that, focus on what really matters which is logic, but rather now you can even just let the logic on the frontend and use the backend strictly for security or a real time ORM. (Senjor will work on giving you as well a nice ReactJS api to access your DB from senjor like you're working on your locally).
5. And more importantly we are working with a path in mind, no mindlessly, no creating by create, two stuff are in mind while creating each line of code here in Senjor, first Atheris, an open source ERP tools built on top of Senjor and ReactJS with full support for Odoo modules, and a private project called Project Horizon (I hope you like this social network when is out). Furthermore we are planning on adding ReactJS as a template system for django, so this way we fully integrate ReactJS finally with Django, making Qwik trembling in fear (so far Qwik is the alternative to django I like the most with its entire SSR strategy and all, but still Django is Django).

A controller in Senjor would look like:

```python
from senjor import models, requests, controllers

# myapp.controllers
class MyModel(controllers.Controllers):
  async def myfield_controller(self, model: models.Model, request: requests.Request, ):
    pass # Do your custom logic here

# myapp.models
class MyModel(models.Model):
  myfield = models.Field()

```

## Architecture

Senjor follows the MVC architecture, but strictly speaking in the initial stages, Senjor will only cover MC or Model Controllers part, views should be handled
by your frontend separately we recommend reactjs as we are going to implement here some features that includes ReactJS.

The models are declared as always but with the difference we don't import from django but instead from senjor to obtain the models.
The controllers on the other hand are to be described following the next syntax:

- field_name_query(self, model: models.Model, request: requests.Request, value: Any)
  - When querying the return value of the function is going to be considered the return value for this field_name, the value is the value the model currently have for this field.
- field_name_mutation(self, model: models.Model, request: requests.Request, value: Any)
  - When mutating you must set the values of the model instance to be the ones you desire, please note that here may be some race conditions as this is asynchronous behavior so report any kind of issues you may find here, the return value of this function should be None as it would be not used at all, the value argument is the value passed by the user or the value expected to be processed.
- field_name_subscription(self, model: models.Model, request: requests.Request, value: Any)
  - When subscribing, the value is the value on the DB, the return value of this function will be returned to the user, if you trigger a change on the model, then this will be possibly trigger other subscription events, perhaps there is some issues if you update this controller's field, but that should be handled by the devs as you perhaps want a recursive like behavior that iterates until a base case.

As you may see we are giving the value in each controller field, but this doesn't mean a query to the DB, is just a django lazy value so unless you read from it, django won't query the db.

## Examples

### Counter App

This is an example of a recursive app that once the user sets a number on the DB using for example the admin site, the subscribed users will receive a countdown from the number the user entered in the db until 0.

```python
# models.py
class MyModel(models.Model):
  counter = models.IntegerField()
# controllers.py
class MyModel(controllers.Controller):
  def counter_subscription(self, model: models.Model, request: requests.Requests, value: int):
    model.counter = value - 1 # just to give an example using value
    model.save() # please note that subscriptions or queries doesn't save by default so you must manually save it to trigger the recursive behavior
    return model.counter # remember that the return value of this function it would be the return value of the field for the subscription
```

### Protected Counter App

```python
# models.py
class MyModel(models.Model):
  counter = models.IntegerField(protected=True)
# controllers.py
class MyModel(controllers.Controller):
  def counter_subscription(self, model: models.Model, request: requests.Requests, value: int):
    model.counter = value - 1 # just to give an example using value
    model.save() # please note that subscriptions or queries doesn't save by default so you must manually save it to trigger the recursive behavior
    return f"{request.user} says: {model.counter}"
```

## Guidelines

We strictly follow the principles of clean coding, for this we are using tools like:

- coverage: For test coverage it should be passing more than 80% to be considered decently ok.
- interrogate: For doc coverage, it should be passing more than 80% to be considered ok.
- trunk: The linters and static testing are included into trunk.
- sphinx: For documenting the code in a more fashionable way.

In regards to code syntax standards, programming style, commit syntax and whatever, we strictly follow rules like the ones defined by:

- conventionalcommits.org
- PEP [specify which versions]
- TODO Continue specifying standards here

## Glossary

- NEER: Same as CRUD but more related to the context RTC apps usually use, New=Create, Erase=Delete, Edit=Update, Read=Read

### Security

There should be a settings to configure senjor as default public or default private, also to define the default authentication framework for all queries, initially we are just going to implement the oauth auth mechanism that integrates well with Keycloak server

## TODO

1. Make graphql available from any channel not just graph-subscribe
2. Create the where ObjectType as a child object type so it allow fully NEER behavior specifically Edit behavior based on the fields given in the where ObjectType
3. Connect the model ObjectType to its respective post_save signal for auto notifying when a model field changes on subscription
4. Add a post_install hook for when the package is installed or a command like senjor install that auto-adds senjor to the INSTALLED_APPS.

## Donate

If you find this project useful, consider supporting it with a donation:

[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.me/etherbeing)

## ChatGPT Feedback on the project

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

| Feature                              | Required for MVP? | Why?                  |
| ------------------------------------ | ----------------- | --------------------- |
| `@require_oauth()` decorator         | Yes               | Easy dev experience   |
| Pluggable token verification backend | Yes               | Flexibility           |
| Config-based setup                   | Yes               | Simplicity            |
| GraphQL context integration          | Yes               | Access to token/user  |
| WS connection param auth             | MVP+              | Required for subs     |
| Subscription auth on connect         | MVP+              | Completes feature set |
| Django permission tie-in             | Optional          | Wider use cases       |
| Strong test suite                    | Yes               | Trust & adoption      |
