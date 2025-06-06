import importlib
import logging
from typing import Any

import socketio
from channels.routing import ProtocolTypeRouter
from django.conf import settings
from django.core.handlers.asgi import ASGIHandler


def setup_sio(
    app: ASGIHandler | socketio.ASGIApp,
    gql_url: str = "/ws/graphql/",
    gql_subscription_channel: str = "graph-subscribe",
):
    """
    Setup socket.io
    This function is used to set up the socket.io server, it uses the django core to configure the server and the app.
    """
    logging.info("Setting up Socket.IO, Channels, Daphne and ASGI...")

    sio = socketio.AsyncServer(
        logger=settings.DEBUG,
        engineio_logger=settings.DEBUG,
        async_mode="asgi",
        namespaces="*",
        cors_allowed_origins="*",
    )

    app = socketio.ASGIApp(sio, app)
    only_sio = socketio.ASGIApp(sio, socketio_path="/socket.io")
    router = ProtocolTypeRouter(
        {
            "http": app,
            "websocket": only_sio,  #
        }
    )
    settings.SIO_ROUTER = router
    settings.SIO_CORE = sio
    settings.SIO_URL = gql_url
    settings.SIO_SUBSCRIPTION_CHANNEL = gql_subscription_channel
    return router


def setup_settings():
    logging.debug("Setting up the settings")
    settings.DEFAULT_AUTO_FIELD = "senjor.core.schema.GQLAutoField"


def setup_senjor(
    official_asgi_app: ASGIHandler, *args: Any, urlpatterns_urlconf: str, **kwargs: Any
):
    """
    Auto configure the whole senjor ecosystem.
    """
    from senjor.urls import urlpatterns

    logging.debug("Injecting the urls and setting up defaults senjor confs ")

    urlpatterns.extend(importlib.import_module(urlpatterns_urlconf).urlpatterns)
    setup_settings()
    return setup_sio(official_asgi_app, *args, **kwargs)
