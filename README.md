# ai-coding-tasks

Small, self-contained coding tasks in the style used to evaluate AI coding
models. Each task has a written specification, a buggy or slow starter, a
reference solution, and a deterministic verifier.

| Task | Skill | What it tests |
| --- | --- | --- |
| `task_01_ttl_cache_bugfix` | Bug fixing | Four interacting bugs in a TTL + LRU cache (recency on hit, inclusive expiry boundary, live-only `len`, purge-before-evict) |
| `task_02_max_overlap_perf` | Algorithms, performance | Turn an O(n^2) maximum-interval-overlap function into O(n log n) for 200k intervals |

## Run

```
pip install -r requirements.txt
bash scripts/check_all.sh            # starters must fail, solutions must pass
IMPL_DIR=solution pytest task_01_ttl_cache_bugfix/tests
IMPL_DIR=/path/to/your/dir pytest task_02_max_overlap_perf/tests
```

Or with Docker: `docker build -t ai-coding-tasks . && docker run --rm ai-coding-tasks`

## How the verifiers work

- They call only the public API, so any correct implementation passes
  (checked with an alternative implementation using different data structures).
- Task 01 compares the cache with an independent list-based model on 150 seeded
  random operation sequences, plus targeted tests for each bug. A hard-coded or
  partial fix fails.
- Task 02 compares against brute force on 200 seeded random inputs and enforces
  a 5 second limit on 200k-interval worst cases (nested, identical, chained).
  A slow solution or one that treats touching intervals as non-overlapping fails.

## Add your own

Task 03 is yours to write. Ideas: add per-key TTL and hit/miss stats to the
cache (feature implementation), or refactor a messy function while keeping all
tests green (refactoring). Copy a task folder as a template.
