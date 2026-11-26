"""Maximum overlap of closed intervals (reference solution, O(n log n))."""


def max_overlap(intervals):
    intervals = list(intervals)
    starts = sorted(s for s, _ in intervals)
    ends = sorted(e for _, e in intervals)
    best = 0
    j = 0  # number of intervals that ended strictly before the current start
    for i, s in enumerate(starts):
        while ends[j] < s:  # closed intervals: end == s still overlaps
            j += 1
        best = max(best, i + 1 - j)
    return best
