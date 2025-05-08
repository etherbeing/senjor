import logging
from typing import Any, Optional
from django.conf import settings
from urllib.parse import parse_qs
from socketio import ASGIApp
from graphql.error.graphql_error import GraphQLError
import socketio
from django.utils.module_loading import import_string



sio: ASGIApp = settings.SIO_CORE
subscription_channel: str = settings.SIO_SUBSCRIPTION_CHANNEL
gql_url: str = settings.SIO_URL
gql_schema = import_string(settings.GRAPHENE.get("SCHEMA")) # this module depends on graphene

@sio.event
async def echo(sid, data):
    await sio.emit('message', data, room=sid)  # Echo back the same message

@sio.event(namespace='/scope')
async def scoped_echo(sid, data):
    await sio.emit('message', data, room=sid, namespace='/scope')  # Echo back the same message


# Subscriptions Managements

class WS:
    def __init__(self, sio: socketio.AsyncServer, room, namespace, default_channel: str) -> None:
        self.sio = sio
        self.room = room
        self.namespace = namespace
        self.default_channel = default_channel

    async def asend(self, data: Any, channel: Optional[str]=None):
        return await self.sio.emit(channel or self.default_channel, data, room=self.room, namespace=self.namespace)
    
    def send(self, data: Any, channel: Optional[str]=None):
        return self.sio.emit(channel or self.default_channel, data, room=self.room, namespace=self.namespace)
    

def normalize_headers(headers: dict) -> dict:
    result = {}

    for key, value in headers.items():
        # Decode bytes to string if necessary
        if isinstance(key, bytes):
            key = key.decode()

        if isinstance(value, bytes):
            value = value.decode()

        # Normalize 'authorization' header
        if key.lower() == 'authorization':
            key = 'Authorization'

        result[key] = value
    return result


async def _manage_result(result, room: str):
    await sio.emit(subscription_channel, result.formatted, room=room, namespace=gql_url)
    
async def _manage_error(errors, room: str):
    for error in errors:
        await sio.emit('error', error.formatted, room=room, namespace=gql_url)

async def subscribe(sid, data):
    environ = sio.get_environ(sid, gql_url)
    query_params = environ and parse_qs(environ.get("QUERY_STRING")) or {}
    results = await gql_schema.subscribe(
        data, 
        root = gql_schema,
        operation_name = query_params.get("operationName", [None])[0],
        context = Dummy(headers=normalize_headers(dict(environ.get('asgi.scope', {}).get('headers'))) if environ else {})
    )
    try:
        if hasattr(results, '__aiter__'):
            async for result in results: # type: ignore
                if result.errors:
                    await _manage_error(result.errors, sid)
                else:
                    await _manage_result(result, sid)     
        else:
            if hasattr(results, 'errors'):
                await _manage_error(results.errors, sid) # type: ignore
            else:
                await _manage_result(results, sid)
    except GraphQLError as ex:
        await _manage_error([ex], room=sid)

sio.on(subscription_channel, handler=subscribe, namespace=gql_url)
