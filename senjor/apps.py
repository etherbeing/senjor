from django.apps import AppConfig

from .signals import senjor_ready


class Senjor(AppConfig):
    name = "senjor"
    verbose_name = "Senjor"

    def ready(self):
        super().ready()

        senjor_ready.send(  # type: ignore
            self,
        )
