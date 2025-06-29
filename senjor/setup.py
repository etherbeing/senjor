import importlib
import logging
from typing import Any

import socketio
from channels.routing import ProtocolTypeRouter
from django.conf import settings
from django.core.handlers.asgi import ASGIHandler

from .apps import Senjor
from .events import SenjorRTC


def setup_sio(
    app: ASGIHandler | socketio.ASGIApp,
    gql_url: str = "/ws/graphql/",
):
    """
    Setup socket.io
    This function is used to set up the socket.io server, it uses the django core to configure the server and the app.
    """
    logging.info("Setting up Socket.IO, Channels, Daphne and ASGI...")

    sio = socketio.AsyncServer(
        logger=logging.getLogger(),
        engineio_logger=logging.getLogger(),
        async_mode="asgi",
        namespaces="*",
        cors_allowed_origins="*",  # FIXME allow only origins configured on the settings make it compatible with ALLOWED_ORIGINS
    )

    app = socketio.ASGIApp(sio, app)
    only_sio = socketio.ASGIApp(sio, socketio_path="/socket.io")
    router = ProtocolTypeRouter(
        {
            "http": app,
            "websocket": only_sio,  #
        }
    )
    # settings.SIO_ROUTER = router
    # settings.SIO_URL = gql_url
    # settings.SIO_SUBSCRIPTION_CHANNEL = gql_subscription_channel
    # this setup the actual ws router handler to deliver the message where it should
    SenjorRTC(sio, gql_url=gql_url).setup()

    return router


def setup_settings():
    logging.debug("Setting up the settings")
    settings.DEFAULT_AUTO_FIELD = "senjor.models.fields.common.GQLAutoField"
    settings.INSTALLED_APPS.insert(
        settings.INSTALLED_APPS.index(Senjor.name), "strawberry.django"
    )
    print(settings.INSTALLED_APPS)


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
