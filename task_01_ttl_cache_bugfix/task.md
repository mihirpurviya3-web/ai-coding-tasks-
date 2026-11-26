# Task 01: Fix the TTL + LRU cache

`starter/ttlcache.py` contains `TTLCache`, a fixed-capacity cache whose entries
also expire after a time-to-live. Users report it "sometimes evicts the wrong
item" and "len() is wrong". Fix the implementation so it follows the
specification below. Do not change the public API.

## Specification

`TTLCache(capacity, ttl, clock=time.monotonic)`

- `capacity` must be a positive int and `ttl` a positive number, otherwise
  `ValueError` is raised.
- `clock()` returns the current time as a float. Tests inject a fake clock.
- `put(key, value)`: stores the value; it expires at `now + ttl`.
  - Overwriting an existing key refreshes its TTL and makes it the most
    recently used entry. It never evicts another entry.
  - Expired entries are removed first. Only if the cache is still over
    capacity is the least recently used live entry evicted.
- `get(key, default=None)`: returns the value, or `default` if the key is
  missing or expired.
  - A successful `get` makes the key the most recently used entry.
  - A `get` does NOT extend the entry's TTL.
- An entry is expired when `now >= expires_at` (exactly at the boundary it is
  already expired).
- `len(cache)` is the number of live (non-expired) entries.

## Constraints

- Standard library only.
- Any correct implementation is accepted (the tests only use the public API).
- Per-operation cost may be O(n); capacity is small in the tests.

## Verify

```
IMPL_DIR=starter  pytest task_01_ttl_cache_bugfix/tests   # should fail
IMPL_DIR=solution pytest task_01_ttl_cache_bugfix/tests   # should pass
```
