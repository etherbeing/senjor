import logging
from collections.abc import Iterable
from types import CoroutineType
from typing import Any, cast
from urllib.parse import parse_qs

from django.conf import settings
from django.utils.module_loading import import_string
from graphene import Schema
from graphql import MapAsyncIterator
from graphql.error.graphql_error import GraphQLError
from socketio import AsyncServer

from senjor.core.attributes import graphql_schema


def normalize_headers(headers: dict[Any, Any]) -> dict[Any, Any]:
    result: dict[Any, Any] = {}

    for key, value in headers.items():
        # Decode bytes to string if necessary
        if isinstance(key, bytes):
            key = key.decode()

        if isinstance(value, bytes):
            value = value.decode()

        # Normalize 'authorization' header
        if key.lower() == "authorization":
            key = "Authorization"

        result[key] = value
    return result


class WS:
    def __init__(
        self, sio: AsyncServer, room: str, namespace: str, default_channel: str
    ) -> None:
        self.sio: AsyncServer = sio
        self.room = room
        self.namespace = namespace
        self.default_channel = default_channel

    async def asend(
        self, data: Any, channel: str | None = None
    ) -> CoroutineType[Any, Any, Any]:
        return cast(
            CoroutineType[Any, Any, Any],
            await self.sio.emit(  # type: ignore
                channel or self.default_channel,
                data,
                room=self.room,
                namespace=self.namespace,
            ),
        )

    def send(
        self, data: Any, channel: str | None = None
    ) -> CoroutineType[Any, Any, Any]:
        return cast(
            CoroutineType[Any, Any, Any],
            self.sio.emit(  # type: ignore
                channel or self.default_channel,
                data,
                room=self.room,
                namespace=self.namespace,
            ),
        )


class SenjorRTC:
    def __init__(
        self,
        app: AsyncServer,
        gql_url: str,
    ) -> None:
        # This GQL Schema runs separately from the synchronous and default HTTP one, this is an specific setup of Senjor
        self.GQL_URL: str = gql_url
        self.GQL_RTC_APP = app

    async def _manage_result(self, result: Any, room: str, event: str):
        await self.GQL_RTC_APP.emit(  # type: ignore
            event,
            result.formatted,
            room=room,
            namespace=self.GQL_URL,
        )

    async def _manage_error(self, errors: Iterable[Any], room: str, event: str):
        for error in errors:
            await self.GQL_RTC_APP.emit(  # type: ignore
                "error", error.formatted, room=room, namespace=self.GQL_URL
            )

    async def __handle_graphql(
        self, event_name: str, sid: str, data: str, *args: Any, **kwargs: Any
    ):
        environ: dict[str, Any] = cast(
            dict[str, Any],
            self.GQL_RTC_APP.get_environ(sid, self.GQL_URL),  # type: ignore
        )
        query_params = environ and parse_qs(environ.get("QUERY_STRING")) or {}
        results: MapAsyncIterator = cast(
            MapAsyncIterator,
            await graphql_schema.execute_async(  # type: ignore
                data,
                root=graphql_schema,
                operation_name=query_params.get("operationName", [None])[0],
                context={
                    "headers": (
                        normalize_headers(
                            dict(environ.get("asgi.scope", {}).get("headers"))
                        )
                        if environ
                        else {}
                    )
                },
            ),
        )
        try:
            if hasattr(results, "__aiter__"):
                async for result in results:
                    if result.errors:
                        await self._manage_error(result.errors, sid, event_name)
                    else:
                        await self._manage_result(result, sid, event_name)
            else:
                if hasattr(results, "errors"):
                    await self._manage_error(results.errors, sid, event_name)  # type: ignore
                else:
                    await self._manage_result(results, sid, event_name)
        except GraphQLError as ex:
            await self._manage_error([ex], room=sid, event=event_name)

    def setup(
        self,
    ):
        logging.info("Setting up the RTC framework of Senjor")
        self.GQL_RTC_APP.on("*", self.__handle_graphql, namespace=self.GQL_URL)  # type: ignore
