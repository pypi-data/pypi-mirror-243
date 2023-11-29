from typing import TYPE_CHECKING
import structlog
import asyncio
from .config import get_redis_url, get_client_tracking_enabled
from functools import wraps
import threading
import redis.asyncio as async_redis

if TYPE_CHECKING:
    from .brokers import Broker


logger = structlog.stdlib.get_logger("brokers.postgres")


# class RedisCounterMap:
#     map_key = "sse_relay_server:channels"

#     def __init__(self, redis_url: str) -> None:
#         self._redis = None

#     # async def increment(self, channel: str) -> None:
#     #     await self._redis.hincrby(self.map_key, channel, 1)

#     # async def decrement(self, channel: str) -> None:
#     #     count = await self._redis.hincrby(self.map_key, channel, -1)
#     #     if count <= 0:
#     #         await self._redis.hdel(self.map_key, channel)

#     async def value(self) -> dict[str, int]:
#         return {k.decode(): int(v) for k, v in await self._redis.hgetall("channels").items()}


class DictCounterMap:
    lock = threading.Lock()

    def __init__(self) -> None:
        self._map = {}

    def increment(self, channel: str):
        with self.lock:
            if channel in self._map:
                self._map[channel] += 1
            else:
                self._map[channel] = 1

    def decrement(self, channel: str):
        with self.lock:
            if channel not in self._map:
                return
            self._map[channel] -= 1
            if self._map[channel] == 0:
                del self._map[channel]

    def value(self):
        return self._map.copy()

class NoopCounterMap:
    def increment(self, channel: str):
        pass

    def decrement(self, channel: str):
        pass

    def value(self):
        return {}

def _get_counter_map():
    # if redis_url := get_redis_url():
    #     # return RedisCounterMap(redis_url)
    #     return DictCounterMap()
    return NoopCounterMap()


_counter = _get_counter_map()
client_tracking_enabled = get_client_tracking_enabled()


def count_clients(func: "Broker.listen"):
    # if not client_tracking_enabled:
    #     return func
    
    return func

    # @wraps(func)
    # async def wrapper(instance: "Broker", channel: str):
    #     try:
    #         #await _counter.increment(channel)
    #         await func(instance, channel)
    #     except asyncio.CancelledError as e:
    #         #await _counter.decrement(channel)
    #         logger.debug(f"Cancelled listening to {channel}")
    #         raise e

    # return wrapper


get_count_value = _counter.value if client_tracking_enabled else lambda: {}
