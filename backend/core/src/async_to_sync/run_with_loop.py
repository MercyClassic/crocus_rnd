import asyncio
import functools
from typing import Callable, TypeVar, Awaitable, ParamSpec


P = ParamSpec('P')
R = TypeVar('R')


def run_with_loop(func: Callable[P, Awaitable[R]]) -> Callable[P, R]:
    loop = asyncio.get_event_loop()

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return loop.run_until_complete(func(*args, **kwargs))

    return wrapper
