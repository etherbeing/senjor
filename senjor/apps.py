from django.apps import AppConfig
from .signals import socketio_ready


class Senjor(AppConfig):
    name = "senjor"
    verbose_name = "Senjor"

    def ready(self):
        super().ready()

        socketio_ready.send(
            self,
        )
