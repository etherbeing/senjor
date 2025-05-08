from django.conf import settings
from channels.routing import ProtocolTypeRouter
from socketio import AsyncServer

SIO_ROUTER: ProtocolTypeRouter # A mapping to all the channels being used (This is not setable and this file is just for referencing purposes)
SIO_CORE: AsyncServer
SIO_URL: str
SIO_SUBSCRIPTION_CHANNEL: str
