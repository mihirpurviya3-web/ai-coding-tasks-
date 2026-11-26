"""Maximum overlap of closed intervals (starter: correct but O(n^2))."""


def max_overlap(intervals):
    intervals = list(intervals)
    best = 0
    for start, _ in intervals:
        count = sum(1 for s, e in intervals if s <= start <= e)
        if count > best:
            best = count
    return best
