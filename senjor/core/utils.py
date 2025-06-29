from asyncio import get_running_loop
from collections.abc import Callable

# from asgiref.sync import sync_to_async
from functools import lru_cache
from typing import Any


@lru_cache
def is_current_async() -> bool:
    """
    Return whether we are in an async context or not
    """
    try:
        get_running_loop()
        return True
    except RuntimeError:
        return False


def run_if_async(sync_runner: Callable[..., Any], async_runner: Callable[..., Any]):
    if is_current_async():
        return async_runner
    else:
        return sync_runner
