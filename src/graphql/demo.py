import asyncio
import graphene
from django.utils.translation import gettext_lazy as _
from typing_extensions import deprecated


from security.graphql import aauthenticate, authenticate
from security.schema import (AppMutation, AppType, AuthMutation,
                             DeleteAppMutation, UserInfo)
from chats.schema import Chat, ChatQuery



# Define Query class
class BaseQuery(graphene.ObjectType):
    dummy = graphene.Field(graphene.String, description=_("Testing unprotected endpoint, DO NOT USE THIS IN PRODUCTION"))
    protected = graphene.Field(graphene.String, description=_("Testing protected endpoint, DO NOT USE THIS IN PRODUCTION"))

    apps = graphene.List(AppType, )
    user_info = graphene.Field(UserInfo,)
    
    def resolve_apps(self, info: graphene.ResolveInfo):
        user = authenticate(info)
        return map(lambda app: AppType(client_id=app.client_id, client_secret=app.client_secret, name=app.app_name),user.app_set.all()) # type: ignore

    def resolve_dummy(self, info):
        return "Hello world"
    
    def resolve_protected(self, info):
        authenticate(info)
        return "Ssshhhh private: **Hello world**"    


# Define Mutation class
class Dummy(graphene.Mutation):
    result = graphene.String()
    def mutate(self, info, name, farewell=False, private=False):
        res = {}
        if farewell:
            res.update(
                result=f"Goodbye {name}"
            )
        else:
            res.update(
                result=f"Hello {name}", 
            )
        if private:
            authenticate(info=info)
            res["result"] = f"Ssshhhh private: **{res['result']}**"
        return Dummy(**res)

    class Arguments:
        name = graphene.String()
        farewell = graphene.Boolean(required=False)
        private = graphene.Boolean(required=False)

class BaseMutation(graphene.ObjectType):
    dummy = Dummy.Field(description=_("Used for testing the mutation graphql (DO NOT USE IN PRODUCTION)"))
    chat = Chat.Field(description=_("Chat related mutations"))
    # Apps
    app = AppMutation.Field(description=_("Handle app creations for API connection"))
    delete_app = DeleteAppMutation.Field(description=_("Delete the app"))
    # End apps

    # Security mutations
    login = AuthMutation.Field(description=_("Handle login requests into the system..."))
    # End security mutations

class BaseSubscription(graphene.ObjectType):
    """Root GraphQL subscription."""
    dummy = graphene.String(up_to=graphene.Int(), description=_("Testing unprotected endpoint, DO NOT USE THIS IN PRODUCTION"))
    protected_dummy = graphene.String(up_to=graphene.Int(), description=_("Testing protected endpoint, DO NOT USE THIS IN PRODUCTION"))
    chat = graphene.Field(Chat, description=_("Chat related subscriptions"))

    async def subscribe_dummy(self, info, up_to):
        for i in range(up_to):
            yield f"Ping #{i}"
            await asyncio.sleep(1)

    async def subscribe_protected_dummy(self, info, up_to):
        aauthenticate(info)
        for i in range(up_to):
            yield f"Ping #{i}"
            await asyncio.sleep(1)

    @deprecated("Using async iterable instead")
    async def _resolve_dummy(self, info, up_to):
        ws = info.context.get('ws')
        for i in range(up_to):
            await ws.send(f"Ping #{i}")
            await asyncio.sleep(1)
        return "Finished dummy subscription ;-)"

    @deprecated("This should return async iterable")
    async def _resolve_protected_dummy(self, info, up_to):
        authenticate(info)
        ws = info.context.get('ws')
        for i in range(up_to):
            await ws.send(f"Ping #{i}")
            await asyncio.sleep(1)
        return "Finished dummy subscription ;-)"