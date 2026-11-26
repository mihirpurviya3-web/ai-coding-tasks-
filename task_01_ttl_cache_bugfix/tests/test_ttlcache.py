"""Verifier for task 01.

Only the public API is used, so any correct implementation passes. Behaviour is
checked with targeted tests and with a differential test against an
independent list-based model on many seeded random operation sequences, which
also rejects hard-coded answers.
"""
import random

import pytest

from ttlcache import TTLCache


class FakeClock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t

    def advance(self, dt):
        self.t += dt


def make(capacity=3, ttl=10):
    clock = FakeClock()
    return TTLCache(capacity, ttl, clock=clock), clock


def test_basic_put_get_and_default():
    c, _ = make()
    c.put("a", 1)
    assert c.get("a") == 1
    assert c.get("missing") is None
    assert c.get("missing", 42) == 42


@pytest.mark.parametrize("capacity,ttl", [(0, 5), (-1, 5), (3, 0), (3, -2)])
def test_invalid_arguments(capacity, ttl):
    with pytest.raises(ValueError):
        TTLCache(capacity, ttl)


def test_expiry_boundary_is_inclusive():
    c, clock = make(ttl=10)
    c.put("a", 1)
    clock.advance(9.99)
    assert c.get("a") == 1
    clock.advance(0.01)  # now == expires_at
    assert c.get("a") is None


def test_get_refreshes_recency():
    c, _ = make(capacity=2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1  # a is now most recent, b is LRU
    c.put("c", 3)
    assert c.get("b") is None
    assert c.get("a") == 1
    assert c.get("c") == 3


def test_get_does_not_extend_ttl():
    c, clock = make(ttl=10)
    c.put("a", 1)
    clock.advance(6)
    assert c.get("a") == 1
    clock.advance(4)  # total 10 since put
    assert c.get("a") is None


def test_len_counts_only_live_entries():
    c, clock = make(capacity=5, ttl=10)
    c.put("a", 1)
    clock.advance(6)
    c.put("b", 2)
    assert len(c) == 2
    clock.advance(5)  # a expired (11 >= 10), b live (5 < 10)
    assert len(c) == 1


def test_put_purges_expired_before_evicting_live_entry():
    c, clock = make(capacity=2, ttl=10)
    c.put("a", 1)          # t=0, expires 10
    clock.advance(6)
    c.put("b", 2)          # t=6, expires 16
    clock.advance(2)
    assert c.get("a") == 1  # t=8: a is MRU, b is LRU
    clock.advance(3)       # t=11: a expired, b live
    c.put("c", 3)
    assert c.get("b") == 2  # live LRU entry must survive
    assert c.get("c") == 3
    assert c.get("a") is None


def test_overwrite_refreshes_ttl_and_never_evicts_others():
    c, clock = make(capacity=2, ttl=10)
    c.put("a", 1)
    c.put("b", 2)
    clock.advance(8)
    c.put("a", 10)  # overwrite at full capacity
    assert len(c) == 2
    clock.advance(5)  # t=13: b expired (10), a live (18)
    assert c.get("a") == 10
    assert c.get("b") is None


class Model:
    """Independent reference model: list ordered LRU -> MRU."""

    def __init__(self, capacity, ttl):
        self.cap, self.ttl, self.items = capacity, ttl, []

    def _purge(self, now):
        self.items = [i for i in self.items if i[2] > now]

    def put(self, k, v, now):
        self._purge(now)
        self.items = [i for i in self.items if i[0] != k]
        self.items.append((k, v, now + self.ttl))
        while len(self.items) > self.cap:
            self.items.pop(0)

    def get(self, k, now):
        self._purge(now)
        for idx, item in enumerate(self.items):
            if item[0] == k:
                self.items.append(self.items.pop(idx))
                return item[1]
        return None

    def length(self, now):
        self._purge(now)
        return len(self.items)


@pytest.mark.parametrize("seed", range(150))
def test_random_operations_match_model(seed):
    rng = random.Random(seed)
    capacity = rng.randint(1, 5)
    ttl = rng.randint(1, 8)
    c, clock = make(capacity, ttl)
    model = Model(capacity, ttl)
    for step in range(120):
        op = rng.random()
        key = rng.choice("abcdefg")
        if op < 0.4:
            value = rng.randint(0, 99)
            c.put(key, value)
            model.put(key, value, clock.t)
        elif op < 0.75:
            assert c.get(key) == model.get(key, clock.t), (seed, step)
        elif op < 0.9:
            assert len(c) == model.length(clock.t), (seed, step)
        else:
            clock.advance(rng.randint(0, 4))
