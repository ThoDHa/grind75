# [Insert Interval](https://leetcode.com/problems/insert-interval/)

**Medium** | **25 minutes** | **Array, Sorting**

**Pattern:** [Interval](../patterns/interval/intuition.md)

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

### Brute Force

```python
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

### Insert and Merge

```python
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

##### Time Complexity: `O(n)`

Each interval is visited at most once. The `pop(i)` and `insert(i, ...)` calls shift only the elements after the overlapping region, and because the overlapping intervals are contiguous the total shifting work stays linear.

##### Space Complexity: `O(1)`

No new list is allocated; the result reuses the input list, ignoring the input and output storage themselves.

#### Key Insights

- Achieves constant auxiliary space by reusing the input list rather than building a new one.
- Slightly harder to read because `pop`/`insert` mutate the list while it is being scanned.
- Appropriate only when destroying the caller's input is acceptable.

### Recursive Merge

```python
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

This recursive approach compares `newInterval` with the first interval and recurses on the rest, peeling one interval per call. There are three cases:

1. The new interval lies entirely before the first interval: prepend it and return.
2. The new interval lies entirely after the first interval: keep the first interval and recurse on the remainder.
3. They overlap: merge them via `min` start and `max` end, then recurse with the merged interval against the remainder.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each interval is consumed by one recursive step. The list slices `intervals[1:]` add linear copying per level, so a strict reading is `O(n^2)`; conceptually each interval is still handled once.

##### Space Complexity: `O(n)`

The recursion reaches depth `O(n)`, and the slicing creates intermediate lists proportional to the input.

#### Key Insights

- Expresses the merge declaratively as a fold over the interval list.
- Not idiomatic here: list slicing and deep recursion make it costlier than the iterative passes.
- Risks exceeding Python's default recursion limit at the upper constraint of `10^4` intervals.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n)` - a single walk over the three regions exploits the already-sorted input.
- **Insert and Merge**: `O(n)` - a linear insertion plus one merge sweep, with no sort.
- **In-Place Modification**: `O(n)` - one pass, but each `pop(i)` shifts elements, so it is `O(n)` overall only because pops are localized to the overlapping region.
- **Recursive Merge**: `O(n)` conceptually (each interval handled once), but `intervals[1:]` slicing per level makes a strict reading `O(n^2)`.

### Space Complexity

- **Brute Force**: `O(n)` - builds a separate merged output list.
- **Insert and Merge**: `O(n)` - builds a combined list and a separate merged output list.
- **In-Place Modification**: `O(1)` - mutates the input list, ignoring input/output storage.
- **Recursive Merge**: `O(n)` - recursion stack depth proportional to the number of intervals.

### Trade-offs

- Brute Force gains optimal linear time and a clear three-region structure without mutating the input, at the cost of an extra output list.
- Insert and Merge gains a familiar mental model (reduce to Merge Intervals) but does redundant work by rebuilding the list and re-checking intervals that never touch the new one.
- In-Place Modification gains `O(1)` auxiliary space by mutating the input in place, giving up readability and a non-destructive contract.
- Recursive Merge gains an elegant declarative form but gives up practicality, risking recursion-depth limits on large inputs.

### When to Use Each

- **Brute Force**: The recommended default; best balance of clarity and efficiency.
- **Insert and Merge**: When you would rather lean on the familiar Merge Intervals sweep than spell out the three regions.
- **In-Place Modification**: When minimizing extra space is critical and mutating the input is acceptable.
- **Recursive Merge**: For academic interest or small inputs only.

### Optimization Notes

- Brute Force is the recommended approach: one linear walk over the three regions, with no sort.
- Insert and Merge trades that direct walk for the familiar Merge Intervals sweep; it stays `O(n)` only because the pre-sorted input lets a linear insertion replace a sort.
- The In-Place Modification approach's in-place `pop`/`insert` operations are convenient but can shift list elements; the savings are in auxiliary space, not in fundamentally lower time cost.
- Every approach hinges on the same three regions: intervals strictly before, intervals overlapping (merged via `min` start and `max` end), and intervals strictly after.
- Avoid the recursive variant for the upper constraint of `10^4` intervals, where deep recursion can exceed Python's default recursion limit.
