"""TTL + LRU cache (reference solution)."""
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

    def _purge(self, now):
        expired = [k for k, (_, exp) in self._data.items() if exp <= now]
        for k in expired:
            del self._data[k]

    def put(self, key, value):
        now = self._clock()
        self._purge(now)  # fix: drop expired entries before evicting live ones
        if key in self._data:
            del self._data[key]
        self._data[key] = (value, now + self._ttl)
        while len(self._data) > self._cap:
            self._data.popitem(last=False)

    def get(self, key, default=None):
        now = self._clock()
        self._purge(now)  # fix: boundary is >=, handled by _purge
        item = self._data.get(key)
        if item is None:
            return default
        self._data.move_to_end(key)  # fix: a hit refreshes recency
        return item[0]

    def __len__(self):
        self._purge(self._clock())  # fix: only live entries count
        return len(self._data)
