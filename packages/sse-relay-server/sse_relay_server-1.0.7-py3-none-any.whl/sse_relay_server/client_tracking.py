from typing import TYPE_CHECKING
import structlog
from .config import get_redis_url, get_client_tracking_enabled
from functools import wraps
import threading
import redis.asyncio as Redis
import asyncio
from contextlib import asynccontextmanager
from typing import Generator


if TYPE_CHECKING:
    from .brokers import Broker

logger = structlog.stdlib.get_logger("client_tracking")


client_tracking_enabled = get_client_tracking_enabled()


class Counter:
    hash_key = "sse_relay_server:channels"

    def __init__(self, redis_url: str):
        self._client = Redis.from_url(redis_url)

    @asynccontextmanager
    async def increment(self, channel: str) -> Generator[None, None, None]:
        logger.debug(f"Incrementing counter for {channel}")
        await self._client.hincrby(self.hash_key, channel, 1)
        try:
            yield
        finally:
            logger.debug(f"Decrementing counter for {channel}")
            await self._client.hincrby(self.hash_key, channel, -1)

    async def value(self) -> dict[str, int]:
        return {
            k.decode(): int(v)
            for k, v in (await self._client.hgetall(self.hash_key)).items()
        }

    async def reset(self) -> None:
        await self._client.delete(self.hash_key)


_counter = Counter(get_redis_url())


def count_clients(func: "Broker.listen"):
    if not client_tracking_enabled:
        return func

    @wraps(func)
    async def wrapper(instance: "Broker", channel: str):
        async with _counter.increment(channel):
            async for event in func(instance, channel):
                yield event

    # @wraps(func)
    # async def wrapper(instance: "Broker", channel: str):
    #     try:
    #         logger.debug(f"Incrementing counter using {_counter.__class__.__name__}")
    #         _counter.increment(channel)
    #         async for event in func(instance, channel):
    #             yield event
    #     except asyncio.CancelledError:
    #         _counter.decrement(channel)
    #         logger.debug(f"Decrementing counter using {_counter.__class__.__name__}")
    #         raise

    return wrapper


async def get_count_value():
    if not client_tracking_enabled:
        return {}
    return await _counter.value()


async def reset_count_value():
    if not client_tracking_enabled:
        return {}
    return await _counter.reset()
