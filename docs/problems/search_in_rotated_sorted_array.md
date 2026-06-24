# [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)

**Medium** | **30 minutes** | **Array, Binary Search**

**Pattern:** [Binary Search](../patterns/binary_search/intuition.md)

**Practice:** [`practice/search_in_rotated_sorted_array/solution.py`](../../practice/search_in_rotated_sorted_array/solution.py)

There is an integer array `nums` sorted in ascending order (with distinct values).

Prior to being passed to your function, `nums` is possibly rotated at an unknown pivot index `k` (`1 <= k < nums.length`) such that the resulting array is `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]` (0-indexed). For example, `[0,1,2,4,5,6,7]` might be rotated at pivot index `3` and become `[4,5,6,7,0,1,2]`.

Given the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.

You must write an algorithm with `O(log n)` runtime complexity.

## Examples

### Example 1

**Input:** nums = `[4,5,6,7,0,1,2]`, target = `0`

**Output:** `4`

### Example 2

**Input:** nums = `[4,5,6,7,0,1,2]`, target = `3`

**Output:** `-1`

### Example 3

**Input:** nums = `[1]`, target = `0`

**Output:** `-1`

## Constraints

- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i] <= 10^4`
- All values of `nums` are unique.
- `nums` is an ascending array that is possibly rotated.
- `-10^4 <= target <= 10^4`

## Solutions

### Linear Scan

```python
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        for i, num in enumerate(nums):
            if num == target:
                return i
        return -1
```

#### Approach

The most direct reading of the problem ignores the rotated-sorted structure entirely and simply walks the array looking for `target`:

1. Iterate over the array, tracking each index.
2. Return the index as soon as an element equals `target`.
3. Return `-1` if the loop finishes without a match.

This always produces the correct answer and is the natural starting point, but it discards the ordering information that makes a logarithmic solution possible. The problem explicitly requires `O(log n)` runtime, so this baseline serves as a correctness reference rather than an acceptable submission.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every element may be examined once in the worst case, when `target` is at the end or absent.

##### Space Complexity: `O(1)`

Only a loop index and the current value are stored.

#### Key Insights

- It is the easiest solution to reason about and verify, which makes it a useful oracle for testing the faster approaches.
- It violates the required `O(log n)` bound, demonstrating exactly what the binary-search refinements need to improve upon.
- It needs no special handling for rotation, single-element arrays, or non-rotated input.

#### Walkthrough

Tracing `Linear Scan` would only show a loop comparing each element, which teaches nothing about the rotated structure. Instead we trace the more instructive `Find Pivot then Binary Search` solution on Example 1: `nums = [4,5,6,7,0,1,2]`, `target = 0`. The indices are `0:4 1:5 2:6 3:7 4:0 5:1 6:2`.

**Phase 1, find the pivot.** First check `nums[left] <= nums[right]`, that is `nums[0]=4 <= nums[6]=2`: false, so the array is rotated and we binary search for the smallest element. Each step compares `nums[mid]` against `nums[right]`: if `nums[mid] > nums[right]` the smallest element is to the right (`left = mid + 1`), otherwise it is at `mid` or to its left (`right = mid`).

| Step | `left` | `right` | `mid` | `nums[mid]` | `nums[right]` | Decision |
|------|--------|---------|-------|-------------|---------------|----------|
| 1 | `0` | `6` | `3` | `7` | `2` | `7 > 2`, pivot right: `left = 4` |
| 2 | `4` | `6` | `5` | `1` | `2` | `1 <= 2`, pivot here/left: `right = 5` |
| 3 | `4` | `5` | `4` | `0` | `1` | `0 <= 1`, pivot here/left: `right = 4` |

Now `left == right == 4`, the loop ends, and `pivot = 4`: the index of the smallest value `0`.

**Phase 2, search the two sorted runs.** The pivot splits the array into `[0, 3] = [4,5,6,7]` and `[4, 6] = [0,1,2]`. Since `pivot > 0`, search the first run `binary_search(0, 3)`:

| Step | `start` | `end` | `mid` | `nums[mid]` | Decision |
|------|---------|-------|-------|-------------|----------|
| 1 | `0` | `3` | `1` | `5` | `5 > 0`: `end = 0` |
| 2 | `0` | `0` | `0` | `4` | `4 > 0`: `end = -1` |

The window empties, so the first run returns `-1`. Now search the second run `binary_search(4, 6)`:

| Step | `start` | `end` | `mid` | `nums[mid]` | Decision |
|------|---------|-------|-------|-------------|----------|
| 1 | `4` | `6` | `5` | `1` | `1 > 0`: `end = 4` |
| 2 | `4` | `4` | `4` | `0` | `0 == 0`: return `4` |

The search returns `4`, which matches the expected Output of `4`.

### Find Pivot then Binary Search

```python
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        def find_pivot() -> int:
            left, right = 0, len(nums) - 1
            if nums[left] <= nums[right]:  # not rotated
                return 0
            while left < right:
                mid = (left + right) // 2
                if nums[mid] > nums[right]:
                    left = mid + 1
                else:
                    right = mid
            return left

        def binary_search(start: int, end: int) -> int:
            while start <= end:
                mid = (start + end) // 2
                if nums[mid] == target:
                    return mid
                elif nums[mid] < target:
                    start = mid + 1
                else:
                    end = mid - 1
            return -1

        pivot = find_pivot()

        if pivot > 0:
            result = binary_search(0, pivot - 1)
            if result != -1:
                return result

        return binary_search(pivot, len(nums) - 1)
```

#### Approach

This solution decomposes the problem into two independent phases, each a familiar binary search:

1. Locate the rotation pivot, the index of the smallest element. If `nums[left] <= nums[right]` the array is not rotated and the pivot is index `0`. Otherwise binary search for the point where the descending step occurs: when `nums[mid] > nums[right]` the pivot lies to the right, so move `left = mid + 1`; otherwise the pivot is at `mid` or to its left, so set `right = mid`.
2. The pivot splits the array into two sorted runs, `[0, pivot - 1]` and `[pivot, n - 1]`. Run a standard binary search over the first run, and if the target is not found there, run it over the second.

Because each run is strictly ascending, the inner searches are ordinary binary searches with no rotation handling, which keeps the logic easy to verify.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

Finding the pivot is one binary search and the value lookup is at most two more, each `O(log n)`, so the total is `O(log n)`.

##### Space Complexity: `O(1)`

Only constant pointer state is used; the helper closures allocate no additional data structures.

#### Key Insights

- A rotated ascending array of distinct values has exactly one pivot where `nums[i - 1] > nums[i]`, and that pivot is the unique minimum.
- Comparing `nums[mid]` against `nums[right]` (rather than `nums[left]`) reliably tells which side the pivot is on during the pivot search.
- Separating pivot-finding from the value lookup keeps each binary search standard, trading a slightly larger constant factor for conceptual clarity.

### Modified Binary Search

```python
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid

            if nums[left] <= nums[mid]:  # left half is sorted
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:  # right half is sorted
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1
```

#### Approach

This solution handles the rotation inside a single binary search. The key observation is that for any `mid`, at least one of the two halves `[left, mid]` and `[mid, right]` is fully sorted:

1. Compute `mid` and return immediately if `nums[mid]` equals `target`.
2. If `nums[left] <= nums[mid]`, the left half is sorted. When `nums[left] <= target < nums[mid]`, the target can only be in that sorted half, so set `right = mid - 1`; otherwise discard it with `left = mid + 1`.
3. Otherwise the right half is sorted. When `nums[mid] < target <= nums[right]`, search right with `left = mid + 1`; otherwise search left with `right = mid - 1`.
4. Return `-1` when the window empties.

Every decision is made against the exact bounds of a provably sorted half, so the target is never discarded by mistake.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

Each iteration eliminates half of the remaining window, giving a single logarithmic pass.

##### Space Complexity: `O(1)`

Only the two pointers and a midpoint are stored.

#### Key Insights

- In a rotated sorted array, at least one half around `mid` is always sorted, which is what lets a single binary search proceed without first locating the pivot.
- Using exact, inclusive-or-exclusive bounds (`nums[left] <= target < nums[mid]` and `nums[mid] < target <= nums[right]`) is what prevents both infinite loops and skipped answers.
- Computing `mid = left + (right - left) // 2` avoids potential integer overflow in languages with fixed-width integers.

## Comparison of Solutions

### Time Complexity

- **Linear Scan**: `O(n)` - examines every element in the worst case.
- **Find Pivot then Binary Search**: `O(log n)` - two or three binary searches of the same order.
- **Modified Binary Search**: `O(log n)` - a single binary-search pass.

### Space Complexity

- **Linear Scan**: `O(1)` - a single loop variable.
- **Find Pivot then Binary Search**: `O(1)` - constant pointer state.
- **Modified Binary Search**: `O(1)` - constant pointer state.

### Trade-offs

- **Linear Scan** is trivially correct and needs no edge-case reasoning, but it fails the required `O(log n)` bound and is unacceptable on large inputs.
- **Find Pivot then Binary Search** keeps each phase a standard binary search, so it is easy to derive and debug and the pivot-finding helper is reusable, at the cost of a worse constant factor from making two passes.
- **Modified Binary Search** completes in one pass for the best constant factor, but its branching is denser and the boundary conditions are easier to get wrong.

### When to Use Each

- **Linear Scan**: Only as a correctness oracle, for tiny inputs, or when the array is known to be unsorted.
- **Find Pivot then Binary Search**: When clarity and maintainability are prioritized, or when teaching the decomposition (Recommended for first attempts).
- **Modified Binary Search**: When the single-pass optimum is required and the denser logic is acceptable.

### Optimization Notes

- The **Modified Binary Search** is the optimal choice when performance matters: it handles rotation within one binary-search pass, eliminating the second traversal of the two-phase approach while preserving `O(log n)` time and `O(1)` space.
- Implementation detail: at each step decide which half is sorted by comparing `nums[left]` to `nums[mid]`, then test whether the target falls inside that sorted range to choose which half to discard, because at least one half is always sorted.
- Interview strategy: present **Linear Scan** to confirm the contract, then derive **Find Pivot then Binary Search** for clarity, and finish with **Modified Binary Search** as the optimization.
- Common pitfall: all binary-search variants must handle non-rotated and single-element arrays, and the boundary comparisons must use the correct inclusive or exclusive bounds to avoid infinite loops or missed targets.
