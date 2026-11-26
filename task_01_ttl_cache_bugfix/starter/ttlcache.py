"""TTL + LRU cache (starter, contains bugs)."""
import time
from collections import OrderedDict


class TTLCache:
    def __init__(self, capacity, ttl, clock=time.monotonic):
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("capacity must be a positive int")
        if ttl <= 0:
            raise ValueError("ttl must be positive")
        self._cap = capacity
        self._ttl = ttl
        self._clock = clock
        self._data = OrderedDict()  # key -> (value, expires_at), LRU first

    def put(self, key, value):
        now = self._clock()
        if key in self._data:
            del self._data[key]
        self._data[key] = (value, now + self._ttl)
        if len(self._data) > self._cap:
            self._data.popitem(last=False)

    def get(self, key, default=None):
        item = self._data.get(key)
        if item is None:
            return default
        value, expires_at = item
        if self._clock() > expires_at:
            del self._data[key]
            return default
        return value

    def __len__(self):
        return len(self._data)
