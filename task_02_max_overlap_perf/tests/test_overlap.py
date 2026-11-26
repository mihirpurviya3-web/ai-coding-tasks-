"""Verifier for task 02.

Correctness is compared against a simple brute force on many seeded random
inputs (including touching endpoints and negative coordinates). Performance is
checked on large inputs with a hard time limit, so a slow-but-correct solution
fails and a hard-coded one cannot pass the randomized checks.
"""
import copy
import random
import signal
import time

import pytest

from overlap import max_overlap


def brute(intervals):
    points = {p for iv in intervals for p in iv}
    return max(
        (sum(1 for s, e in intervals if s <= p <= e) for p in points), default=0
    )


class Timeout(Exception):
    pass


def run_with_limit(fn, seconds):
    def handler(signum, frame):
        raise Timeout()

    old = signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        start = time.perf_counter()
        result = fn()
        return result, time.perf_counter() - start
    except Timeout:
        pytest.fail(f"exceeded {seconds}s time limit")
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)


def test_empty_and_single():
    assert max_overlap([]) == 0
    assert max_overlap([(5, 5)]) == 1


def test_touching_endpoints_overlap():
    assert max_overlap([(1, 3), (3, 5)]) == 2
    assert max_overlap([(1, 2), (3, 4)]) == 1


def test_nested_and_identical():
    assert max_overlap([(0, 10), (2, 3), (2, 3), (5, 6)]) == 3
    assert max_overlap([(1, 1)] * 7) == 7


def test_accepts_tuples_iterables_and_does_not_mutate():
    data = [(4, 9), (1, 5), (6, 7)]
    snapshot = copy.deepcopy(data)
    assert max_overlap(iter(data)) == 2
    assert max_overlap(data) == 2
    assert data == snapshot


@pytest.mark.parametrize("seed", range(200))
def test_random_small_matches_brute(seed):
    rng = random.Random(seed)
    n = rng.randint(0, 25)
    span = rng.choice([5, 20, 100])
    data = []
    for _ in range(n):
        s = rng.randint(-span, span)
        data.append((s, s + rng.randint(0, span)))
    assert max_overlap(data) == brute(data), data


def test_large_random_is_fast_and_stable():
    rng = random.Random(12345)
    data = []
    for _ in range(200_000):
        s = rng.randint(-10**9, 10**9)
        data.append((s, s + rng.randint(0, 10**7)))
    first, elapsed = run_with_limit(lambda: max_overlap(data), 5)
    assert first >= 1
    assert max_overlap(data) == first  # deterministic result


def test_large_worst_cases_are_fast():
    n = 200_000
    nested = [(i, 10**9 - i) for i in range(n)]
    same = [(7, 7)] * n
    chain = [(i, i + 1) for i in range(n)]
    got, _ = run_with_limit(lambda: max_overlap(nested), 5)
    assert got == n
    got, _ = run_with_limit(lambda: max_overlap(same), 5)
    assert got == n
    got, _ = run_with_limit(lambda: max_overlap(chain), 5)
    assert got == 2
