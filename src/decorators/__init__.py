from django.conf import settings
from graphene import ObjectType, Mutation
from socketio import AsyncServer

sio: AsyncServer = settings.SIO_CORE

def route(path: str, protected: bool=False, channel: str="message") -> ObjectType|Mutation:
    """
    This route decorator is a convenience decorator that allows you to register a function as a socket.io event handler. It is used to define the endpoint for the socket.io server.
    :param path: This is the socket.io or websocket namespace used to identify this endpoint.
    :param channel: For verbosity purposes this is actually the name of the event, by default the event is "message" so when using for example postman the the events you should be listening is by default "message".
    :return: An object type or mutation that is going to be given back to the user.
    :rtype: ObjectType|Mutation
    """
    def decorated(func: ObjectType|Mutation) -> ObjectType|Mutation:
        sio.on(
            channel,
            func,
            path
        )
        return func
    return decorated

    