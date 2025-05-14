import importlib
from typing import Callable

import socketio
from channels.routing import ProtocolTypeRouter
from django.conf import settings
from django.core.handlers.asgi import ASGIHandler
from django.urls import URLPattern


def setup_sio(app: ASGIHandler, gql_url: str = '/ws/graphql/', gql_subscription_channel: str = "graph-subscribe"):
    """
    Setup socket.io
    This function is used to set up the socket.io server, it uses the django core to configure the server and the app.
    """
    sio = socketio.AsyncServer(
        logger=settings.DEBUG,
        engineio_logger=settings.DEBUG,
        async_mode='asgi',
        namespaces="*",
        cors_allowed_origins='*',
    )

    app = socketio.ASGIApp(sio, app)
    only_sio = socketio.ASGIApp(sio, socketio_path="/socket.io")
    router = ProtocolTypeRouter(
        {
            'http': app,
            "websocket": only_sio,  #
        }
    )
    settings.SIO_ROUTER = router
    settings.SIO_CORE = sio
    settings.SIO_URL = gql_url
    settings.SIO_SUBSCRIPTION_CHANNEL = gql_subscription_channel
    return router


def setup_senjor(official_asgi_app: ASGIHandler, *args, urlpatterns_urlconf: str, **kwargs):
    """
    Auto configure the whole senjor ecosystem.
    """
    from senjor.urls import urlpatterns
    urlpatterns.extend(importlib.import_module(urlpatterns_urlconf).urlpatterns)
    return setup_sio(official_asgi_app, *args, **kwargs)
