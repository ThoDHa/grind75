# [Insert Interval](https://leetcode.com/problems/insert-interval/)

**Medium** | **25 minutes** | **Array, Sorting**

**Pattern:** [Interval](../patterns/interval/intuition.md)

**Algorithm:** [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm)

**Practice:** [`practice/insert_interval/solution.py`](../../practice/insert_interval/solution.py)

You are given an array of non-overlapping intervals where `intervals[i] = [starti, endi]` represent the start and the end of the `ith` interval and `intervals` is sorted in ascending order by `starti`. You are also given an interval `newInterval = [start, end]` that represents the start and end of another interval.

Insert `newInterval` into `intervals` such that `intervals` is still sorted in ascending order by `starti` and `intervals` still does not have any overlapping intervals (merge overlapping intervals if necessary).

Return `intervals` after the insertion.

## Examples

### Example 1

**Input:** `intervals = [[1,3],[6,9]]`, `newInterval = [2,5]`

**Output:** `[[1,5],[6,9]]`

### Example 2

**Input:** `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]`, `newInterval = [4,8]`

**Output:** `[[1,2],[3,10],[12,16]]`

**Explanation:** Because the new interval `[4,8]` overlaps with `[3,5]`, `[6,7]`, `[8,10]`.

### Example 3

**Input:** `intervals = []`, `newInterval = [5,7]`

**Output:** `[[5,7]]`

## Constraints

- `0 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= starti <= endi <= 10^5`
- `intervals` is sorted by `starti` in ascending order.
- `newInterval.length == 2`
- `0 <= start <= end <= 10^5`

## Solutions

### Linear Scan and Merge

```python
from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        merged = []
        i, n = 0, len(intervals)
        # Add all intervals that end before newInterval starts
        while i < n and intervals[i][1] < newInterval[0]:
            merged.append(intervals[i])
            i += 1
        # Absorb every interval that overlaps newInterval
        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        merged.append(newInterval)
        # Add all intervals that start after newInterval ends
        while i < n:
            merged.append(intervals[i])
            i += 1
        return merged
```

#### Overlap Condition

Interval \(i\) overlaps the new interval \([s, e]\) exactly when:

$$
\max(a_i, s) \le \min(b_i, e)
$$

```text
intervals[i] overlaps newInterval  if and only if
    max(intervals[i][0], newInterval[0]) <= min(intervals[i][1], newInterval[1])
```

Because the input is sorted by start and never overlaps itself, that single
condition partitions the list into three contiguous runs — which is precisely
the three `while` loops:

$$
\underbrace{b_i < s}_{\text{strictly before}}
\qquad
\underbrace{a_i \le e \ \wedge \ b_i \ge s}_{\text{overlapping}}
\qquad
\underbrace{a_i > e}_{\text{strictly after}}
$$

```text
strictly before: intervals[i][1] <  newInterval[0]
overlapping:     intervals[i][0] <= newInterval[1]
                 and intervals[i][1] >= newInterval[0]
strictly after:  intervals[i][0] >  newInterval[1]
```

Each loop tests only the one side that can still change, since the previous loop
has already established the other. The middle run absorbs into a single
interval:

$$
\Bigl[\ \min\bigl(s,\ \min_i a_i\bigr),\ \ \max\bigl(e,\ \max_i b_i\bigr)\ \Bigr]
$$

```text
newInterval = [min(newInterval[0], min of intervals[i][0]),
               max(newInterval[1], max of intervals[i][1])]
              (min and max taken over the overlapping run only)
```

The runs are contiguous only because the input is disjoint and sorted; that is
what makes one pass sufficient and why no sort is needed here, unlike in Merge
Intervals. Both boundary tests use non-strict comparison, so touching intervals
merge rather than staying separate.

#### Approach

The intervals arrive already sorted by start, so the most direct idea is to walk the list once and handle `newInterval` by hand, splitting the work into the three regions it creates: the intervals before it, the intervals it overlaps, and the intervals after it. Each region gets its own `while` loop.

1. Copy every interval that ends strictly before `newInterval` starts (`intervals[i][1] < newInterval[0]`); these are untouched.
2. Absorb every interval that overlaps `newInterval` (`intervals[i][0] <= newInterval[1]`), growing `newInterval` via `min` of starts and `max` of ends, then append the grown interval once.
3. Copy every remaining interval; all of them start strictly after `newInterval` ends.

The touching condition uses `<=` so intervals that share an endpoint, such as `[1,5]` and `[5,8]`, merge into `[1,8]`. No sort is needed because the input is already ordered.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each interval is examined by exactly one of the three loops, so the total work is linear.

##### Space Complexity: `O(n)`

The `merged` output list holds up to `n + 1` intervals; no other auxiliary storage grows with the input.

#### Key Insights

- Solves the problem head-on by handling the three regions (before, overlapping, after) rather than reducing it to another problem.
- Exploiting the guaranteed sorted order means one linear walk suffices, with no sort.
- Handles every edge case cleanly: empty input, insertion before all or after all intervals, and full overlap.

#### Walkthrough

Let us watch the Linear Scan and Merge run on Example 1: `intervals = [[1,3],[6,9]]`, `newInterval = [2,5]`. The expected output is `[[1,5],[6,9]]`.

We start with `merged = []`, `i = 0`, and `n = 2`. The trace below shows which of the three loops fires at each step and what changes.

| Step | Loop | Interval at `i` | Condition checked | Action | `newInterval` | `i` | `merged` |
|------|------|-----------------|-------------------|--------|---------------|-----|----------|
| 1 | loop 1 (before) | `[1,3]` | `intervals[0][1] < newInterval[0]`: `3 < 2`? No | loop 1 stops, no append | `[2,5]` | `0` | `[]` |
| 2 | loop 2 (overlap) | `[1,3]` | `intervals[0][0] <= newInterval[1]`: `1 <= 5`? Yes | absorb: start `min(2,1)=1`, end `max(5,3)=5` | `[1,5]` | `1` | `[]` |
| 3 | loop 2 (overlap) | `[6,9]` | `intervals[1][0] <= newInterval[1]`: `6 <= 5`? No | loop 2 stops | `[1,5]` | `1` | `[]` |
| 4 | append | : | : | append grown `newInterval` | `[1,5]` | `1` | `[[1,5]]` |
| 5 | loop 3 (after) | `[6,9]` | `i < n`: `1 < 2`? Yes | append `[6,9]`, advance `i` | `[1,5]` | `2` | `[[1,5],[6,9]]` |

Loop 3's condition `i < n` is now `2 < 2`, which is false, so the loop ends. The function returns `merged = [[1,5],[6,9]]`, which matches the expected Output `[[1,5],[6,9]]`.

### Insert and Merge

```python
from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        # Drop newInterval into its sorted slot, then it is just Merge Intervals.
        i = 0
        while i < len(intervals) and intervals[i][0] < newInterval[0]:
            i += 1
        combined = intervals[:i] + [newInterval] + intervals[i:]

        merged = []
        for interval in combined:
            # No overlap with the last kept interval: start a new one.
            if not merged or merged[-1][1] < interval[0]:
                merged.append(interval)
            else:
                # Overlap: extend the last interval's end.
                merged[-1][1] = max(merged[-1][1], interval[1])
        return merged
```

#### Approach

Instead of reasoning about three regions, notice that inserting an interval into a sorted, non-overlapping list and re-merging is exactly the Merge Intervals problem with one extra interval. Drop `newInterval` into its sorted position, then run the standard merge sweep over the combined list. The input is already sorted, so finding the slot is a linear scan and no sort is needed.

1. Scan to the first interval whose start is not less than `newInterval`'s start, and splice `newInterval` in there so the combined list stays sorted by start.
2. Sweep the combined list once: append each interval, or, when it overlaps the last kept interval, extend that interval's end via `max`.

The overlap test `merged[-1][1] < interval[0]` treats a shared endpoint as an overlap, so touching intervals such as `[1,5]` and `[5,8]` merge into `[1,8]`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The insertion scan, the splice, and the merge sweep each touch every interval at most once.

##### Space Complexity: `O(n)`

The `combined` list and the `merged` output each hold up to `n + 1` intervals.

#### Key Insights

- Reframes the task as Merge Intervals, reusing a sweep you may already know instead of deriving the region logic from scratch.
- Recognizing that the input is pre-sorted is what lets a linear insertion replace a full sort.
- It does redundant work next to the direct walk: it rebuilds the list and re-checks intervals that never touch `newInterval`.

### In-Place Modification

```python
from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        i = 0
        # Find the position to insert
        while i < len(intervals) and intervals[i][1] < newInterval[0]:
            i += 1
        # Merge overlapping intervals in-place
        while i < len(intervals) and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            intervals.pop(i)
        intervals.insert(i, newInterval)
        return intervals
```

#### Approach

This variant mutates the input list directly. It advances past the intervals that precede the overlap, then repeatedly absorbs and `pop`s each overlapping interval into `newInterval`, and finally inserts the merged interval at the gap that remains.

1. Advance `i` past every interval ending before `newInterval` starts.
2. While the interval at `i` overlaps `newInterval`, fold it into `newInterval` and `pop` it from the list.
3. Insert the merged `newInterval` at index `i`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The scan itself visits each interval at most once, but every `pop(i)` shifts the entire tail of the list left by one position. Absorbing `k` overlapping intervals with `n - k` intervals after them costs `O(k × (n - k))` in shifting alone, which is `O(n^2)` in the worst case, such as a new interval that swallows the first half of the list. The final `insert(i, ...)` adds one more `O(n)` shift.

##### Space Complexity: `O(1)`

No new list is allocated; the result reuses the input list, ignoring the input and output storage themselves.

#### Key Insights

- Achieves constant auxiliary space by reusing the input list rather than building a new one.
- The space saving has a time cost: each `pop(i)` shifts the tail of the list, degrading the worst case to quadratic.
- Slightly harder to read because `pop`/`insert` mutate the list while it is being scanned.
- Appropriate only when destroying the caller's input is acceptable.

### Binary Search for the Overlap Window

```python
from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        n = len(intervals)

        # Leftmost index whose interval ends at or after newInterval starts.
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if intervals[mid][1] >= newInterval[0]:
                hi = mid
            else:
                lo = mid + 1
        first = lo

        # Rightmost index whose interval starts at or before newInterval ends.
        lo, hi = -1, n - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if intervals[mid][0] <= newInterval[1]:
                lo = mid
            else:
                hi = mid - 1
        last = lo

        if first > last:
            # Empty window: nothing overlaps, newInterval slots in at index first.
            return intervals[:first] + [newInterval] + intervals[first:]

        merged = [
            min(newInterval[0], intervals[first][0]),
            max(newInterval[1], intervals[last][1]),
        ]
        return intervals[:first] + [merged] + intervals[last + 1:]
```

#### Approach

Because the intervals are sorted by start and do not overlap, their end values are also in ascending order: each interval ends before the next one begins. That means two boundary [binary searches](https://en.wikipedia.org/wiki/Binary_search_algorithm) can locate the block of intervals that touch `newInterval`, replacing the linear scans of the earlier approaches with `O(log n)` lookups.

An interval overlaps `newInterval` exactly when both `intervals[i][1] >= newInterval[0]` (it does not end before the new one starts) and `intervals[i][0] <= newInterval[1]` (it does not start after the new one ends). Each condition gets its own search:

1. The first search runs over the ascending end values and finds `first`, the leftmost index with `intervals[i][1] >= newInterval[0]`. Ends before `first` are too small to overlap; ends from `first` onward all satisfy the predicate, so the predicate flips exactly once and the search is valid.
2. The second search runs over the ascending start values and finds `last`, the rightmost index with `intervals[i][0] <= newInterval[1]`. Starts after `last` are too large to overlap. The midpoint uses `(lo + hi + 1) // 2` because this search rounds toward the right boundary; rounding down would loop forever when `lo` and `hi` are adjacent.
3. Since both predicates flip once over the sorted list, the overlapping intervals are exactly the contiguous window `[first, last]`. If `first > last`, the window is empty and `newInterval` overlaps nothing: it slots in unchanged at index `first`. Otherwise one merged interval spans `min` of the starts at the window's left edge and `max` of the ends at its right edge, and the result is the untouched prefix, the merged interval, and the untouched suffix.

Both comparisons use `>=` and `<=` so intervals that merely touch `newInterval` at an endpoint, such as `[1,5]` against a new `[5,8]`, land inside the window and merge.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The two binary searches cost `O(log n)`, but the return statement slices the prefix and suffix into a new list, copying up to `n` interval references. The copying dominates, so the overall bound stays `O(n)`: the searches reduce the comparison work, not the asymptotic total. This approach is about practicing the boundary-search technique, not about beating the linear scan.

##### Space Complexity: `O(n)`

The result list built from the prefix slice, the merged interval, and the suffix slice holds up to `n + 1` intervals; the searches themselves use constant extra space.

#### Key Insights

- Boundary binary searches are predicate design: choose a condition that is monotone over the sorted list, then find where it flips. The left edge is the first index where `end >= newInterval[0]` becomes true; the right edge is the last index where `start <= newInterval[1]` is still true.
- The rightmost-flavored search needs the `(lo + hi + 1) // 2` midpoint; the leftmost flavor rounds down. Mixing them up produces an infinite loop on adjacent bounds.
- Sortedness plus non-overlap make both the starts and the ends monotone, which is exactly why the overlapping intervals form one contiguous window rather than scattered matches.
- There is no asymptotic win here: any solution that returns a new list of up to `n + 1` intervals must spend `O(n)` building it. A true `O(log n)` algorithm exists only when the answer avoids the rebuild, such as counting the overlapping intervals (`last - first + 1`), reporting the merged interval's bounds, or testing whether `newInterval` overlaps anything at all.

### Recursive Merge

```python
from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        if not intervals:
            return [newInterval]
        if newInterval[1] < intervals[0][0]:
            return [newInterval] + intervals
        elif newInterval[0] > intervals[0][1]:
            return [intervals[0]] + self.insert(intervals[1:], newInterval)
        else:
            merged = [min(newInterval[0], intervals[0][0]), max(newInterval[1], intervals[0][1])]
            return self.insert(intervals[1:], merged)
```

#### Approach

This [recursive](https://en.wikipedia.org/wiki/Recursion_(computer_science)) approach compares `newInterval` with the first interval and recurses on the rest, peeling one interval per call. There are three cases:

1. The new interval lies entirely before the first interval: prepend it and return.
2. The new interval lies entirely after the first interval: keep the first interval and recurse on the remainder.
3. They overlap: merge them via `min` start and `max` end, then recurse with the merged interval against the remainder.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each interval is consumed by one recursive step, but every level copies the remainder of the list through the `intervals[1:]` slice, adding linear work per interval. Conceptually each interval is handled once; the slicing is what pushes the bound to `O(n^2)`.

##### Space Complexity: `O(n^2)`

The recursion reaches depth `O(n)`, and each frame holds its own `intervals[1:]` slice copy alive until the recursion below it returns, so the live slices across the stack total `O(n^2)` in the worst case.

#### Key Insights

- Expresses the merge declaratively as a fold over the interval list.
- Not idiomatic here: list slicing and deep recursion make it costlier than the iterative passes.
- Risks exceeding Python's default recursion limit at the upper constraint of `10^4` intervals.

## Comparison of Solutions

### Time Complexity

- **Linear Scan and Merge**: `O(n)` - a single walk over the three regions exploits the already-sorted input.
- **Insert and Merge**: `O(n)` - a linear insertion plus one merge sweep, with no sort.
- **In-Place Modification**: `O(n^2)` worst case - each `pop(i)` shifts the entire tail of the list, so absorbing many overlapping intervals costs quadratic shifting.
- **Binary Search for the Overlap Window**: `O(n)` - the two boundary searches take only `O(log n)`, but slicing the prefix and suffix into the result still copies up to `n` intervals.
- **Recursive Merge**: `O(n^2)` - each interval is handled once, but the `intervals[1:]` copy at every level adds linear work per step.

### Space Complexity

- **Linear Scan and Merge**: `O(n)` - builds a separate merged output list.
- **Insert and Merge**: `O(n)` - builds a combined list and a separate merged output list.
- **In-Place Modification**: `O(1)` - mutates the input list, ignoring input/output storage.
- **Binary Search for the Overlap Window**: `O(n)` - builds the result from prefix, merged-window, and suffix copies.
- **Recursive Merge**: `O(n^2)` worst case - `O(n)` recursion depth where each frame keeps its own `intervals[1:]` slice copy alive.

### Trade-offs

- Linear Scan and Merge gains optimal linear time and a clear three-region structure without mutating the input, at the cost of an extra output list.
- Insert and Merge gains a familiar mental model (reduce to Merge Intervals) but does redundant work by rebuilding the list and re-checking intervals that never touch the new one.
- In-Place Modification gains `O(1)` auxiliary space by mutating the input in place, giving up readability, a non-destructive contract, and the linear time bound (tail-shifting pops make the worst case quadratic).
- Binary Search for the Overlap Window gains `O(log n)` comparison work and a reusable boundary-search technique, but the output rebuild keeps the overall bound at `O(n)`, so it offers no asymptotic advantage over the linear scan.
- Recursive Merge gains an elegant declarative form but gives up practicality, risking recursion-depth limits on large inputs.

### When to Use Each

- **Linear Scan and Merge**: The recommended default; best balance of clarity and efficiency.
- **Insert and Merge**: When you would rather lean on the familiar Merge Intervals sweep than spell out the three regions.
- **In-Place Modification**: When minimizing extra space is critical and mutating the input is acceptable.
- **Binary Search for the Overlap Window**: When you want to practice boundary binary searches, or when the real question is locating or counting the overlapping intervals rather than rebuilding the list.
- **Recursive Merge**: For academic interest or small inputs only.

### Optimization Notes

- Linear Scan and Merge is the recommended approach: one linear walk over the three regions, with no sort.
- Insert and Merge trades that direct walk for the familiar Merge Intervals sweep; it stays `O(n)` only because the pre-sorted input lets a linear insertion replace a sort.
- The In-Place Modification approach's `pop`/`insert` operations shift the tail of the list on every call, so the auxiliary-space saving is paid for with a quadratic worst-case time bound.
- Binary Search for the Overlap Window cuts the comparisons to `O(log n)` but not the copying; it becomes a genuine `O(log n)` algorithm only when the answer does not require rebuilding the list, such as counting or locating the overlapping intervals.
- Every approach hinges on the same three regions: intervals strictly before, intervals overlapping (merged via `min` start and `max` end), and intervals strictly after.
- Avoid the recursive variant for the upper constraint of `10^4` intervals, where deep recursion can exceed Python's default recursion limit.
