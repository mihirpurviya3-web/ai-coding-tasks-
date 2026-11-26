# Task 02: Make `max_overlap` fast

`starter/overlap.py` has `max_overlap(intervals)`. It returns the right answer
but is far too slow on large inputs. Rewrite it so it handles 200,000
intervals comfortably, without changing behaviour.

## Specification

- `intervals` is a list (or any iterable of pairs) of `(start, end)` integers
  with `start <= end`. Intervals are **closed**: `[1, 3]` and `[3, 5]` overlap
  at the point 3.
- Return the largest number of intervals that contain a common point.
- Return `0` for an empty input.
- Do not mutate the input.

## Constraints

- Standard library only.
- Input size up to 200,000 intervals; coordinates may be large (up to 10**9) and
  may be negative. The verifier allows 5 seconds for the large case.
- Any correct algorithm is accepted.

## Verify

```
IMPL_DIR=starter  pytest task_02_max_overlap_perf/tests   # should fail (too slow)
IMPL_DIR=solution pytest task_02_max_overlap_perf/tests   # should pass
```
