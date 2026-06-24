# [Binary Search](https://leetcode.com/problems/binary-search/)

**Easy** | **15 minutes** | **Binary Search**

**Pattern:** [Binary Search](../patterns/binary_search/intuition.md)

**Practice:** [`practice/binary_search/solution.py`](../../practice/binary_search/solution.py)

Given an array of integers `nums` which is sorted in ascending order, and an
integer `target`, write a function to search `target` in `nums`. If `target`
exists, then return its index. Otherwise, return -1.

You must write an algorithm with `O(log n)` runtime complexity.

## Examples

### Example 1

**Input:** `nums = [-1,0,3,5,9,12]`, `target = 9`

**Output:** `4`

**Explanation:** `9` exists in `nums` and its index is `4`.

### Example 2

**Input:** `nums = [-1,0,3,5,9,12]`, `target = 2`

**Output:** `-1`

**Explanation:** `2` does not exist in `nums` so return `-1`.

## Constraints

- `1 <= nums.length <= 10^4`
- `-10^4 < nums[i], target < 10^4`
- All the integers in `nums` are unique.
- `nums` is sorted in ascending order.

## Solutions

### Linear Scan

```python
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        for i in range(len(nums)):
            if nums[i] == target:
                return i
        return -1
```

#### Approach

Before exploiting the sorted order, the most direct idea is to look at every element in turn and report the first index that matches `target`. This works on any array, sorted or not, and needs no insight beyond a single pass:

1. Iterate over the indices `0` to `len(nums) - 1`.
2. If `nums[i]` equals `target`, return `i` immediately.
3. If the loop finishes without a match, `target` is absent, so return `-1`.

Because the array is scanned left to right, the first index returned is the only index for any value (the constraints guarantee unique elements).

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- In the worst case the target is at the last position or absent, so all `n` elements are examined.
- This does not meet the problem's required `O(log n)` bound; it is the baseline to improve upon.

##### Space Complexity: `O(1)`

- Only the loop index is stored, so memory usage is constant.

#### Key Insights

- This is the most self-derivable approach: it ignores the sorted order entirely and simply checks each element.
- It is correct for every input but wastes the structure the problem hands us, motivating the logarithmic binary search below.
- The `O(n)` runtime violates the problem's stated requirement, so it serves only as a baseline rather than an accepted answer.

### Iterative Binary Search

```python
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1
```

#### Approach

The array is sorted, so a single comparison against the middle element reveals which half of the remaining range can still contain the target. Maintaining an inclusive search interval `[left, right]` and repeatedly halving it is the most direct way to express this:

1. Initialize `left` to `0` and `right` to `len(nums) - 1`, bounding the full array.
2. While the interval is non-empty (`left <= right`):
   - Compute the middle index as `left + (right - left) // 2`.
   - If `nums[mid]` equals `target`, return `mid`.
   - If `nums[mid]` is less than `target`, the answer must lie to the right, so set `left = mid + 1`.
   - Otherwise the answer lies to the left, so set `right = mid - 1`.
3. When the loop exits, the interval is empty and the target was never found, so return `-1`.

Each iteration discards half of the candidates, so the interval shrinks to a single element in logarithmic time.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

- Every iteration halves the size of the search interval.
- For an array of length `n`, at most `log₂(n)` iterations are needed before the interval is empty.
- This satisfies the problem's required logarithmic runtime.

##### Space Complexity: `O(1)`

- Only the two index variables `left` and `right` are stored.
- No recursion or auxiliary data structure is used, so memory usage is constant.

#### Key Insights

- The inclusive interval `[left, right]` with the `left <= right` loop condition handles the single-element interval correctly, which is where off-by-one bugs usually appear.
- Computing `mid` as `left + (right - left) // 2` avoids the integer overflow that `(left + right) // 2` can cause in fixed-width integer languages.
- The constant space makes this the standard production form of binary search.

### Recursive Binary Search

```python
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        return self._binary_search(nums, target, 0, len(nums) - 1)

    def _binary_search(
        self, nums: List[int], target: int, left: int, right: int
    ) -> int:
        if left > right:
            return -1

        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            return self._binary_search(nums, target, mid + 1, right)
        else:
            return self._binary_search(nums, target, left, mid - 1)
```

#### Approach

This is the same halving strategy expressed through recursion, where each call owns one subinterval and delegates the smaller subinterval to the next call:

1. The public `search` method seeds the recursion with the full range `[0, len(nums) - 1]`.
2. The helper `_binary_search` handles one interval at a time:
   - Base case: if `left > right`, the interval is empty and the target is absent, so return `-1`.
   - Compute `mid` and compare `nums[mid]` with `target`.
   - If they are equal, return `mid`.
   - If `nums[mid] < target`, recurse on the right half `[mid + 1, right]`.
   - Otherwise recurse on the left half `[left, mid - 1]`.

Because each call passes a strictly smaller interval, the recursion is guaranteed to terminate.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

- Each recursive call halves the interval, so the recursion depth is at most `log₂(n)`.
- A constant amount of work is done per call, giving logarithmic total time.

##### Space Complexity: `O(log n)`

- The recursion call stack grows to a depth of `log₂(n)`.
- This is the only extra memory used, but it is not constant like the iterative form.

#### Key Insights

- The recursion mirrors the divide-and-conquer structure of binary search directly, which some readers find clearer than the loop.
- The base case `left > right` is the recursive analogue of the iterative loop terminating, and getting it right is essential to avoid infinite recursion.
- The call stack means this form is not strictly constant space; very large inputs theoretically risk deep recursion, though `log₂(10^4)` is tiny in practice.

### Library Bisect

```python
import bisect
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        index = bisect.bisect_left(nums, target)
        if index < len(nums) and nums[index] == target:
            return index
        return -1
```

#### Approach

Python's `bisect` module performs binary search over a sorted sequence, so the work reduces to a single library call plus a membership check:

1. `bisect.bisect_left(nums, target)` returns the leftmost index where `target` could be inserted to keep `nums` sorted.
2. If that index is within bounds and `nums[index]` equals `target`, the target is present, so return `index`.
3. Otherwise `target` is not in the array, so return `-1`.

The bounds and equality check are required because `bisect_left` returns an insertion point even when the target is absent.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

- `bisect_left` runs a binary search internally, taking logarithmic time.
- The follow-up bounds and equality check is constant time.

##### Space Complexity: `O(1)`

- `bisect_left` operates in place over the existing list and allocates no auxiliary structure.

#### Key Insights

- This is the idiomatic Python way to binary-search a sorted list and is the least error-prone to write under time pressure.
- The insertion-point semantics of `bisect_left` mean an explicit presence check is mandatory; returning the raw index would wrongly report absent targets as found.
- It relies on the standard library to do the core search, so it is included after the from-scratch approaches that demonstrate the underlying algorithm.

## Comparison of Solutions

### Time Complexity

- **Linear Scan**: `O(n)` - checks every element in the worst case.
- **Iterative Binary Search**: `O(log n)` - halves the interval each iteration.
- **Recursive Binary Search**: `O(log n)` - halves the interval each call.
- **Library Bisect**: `O(log n)` - `bisect_left` performs an internal binary search.

### Space Complexity

- **Linear Scan**: `O(1)` - only the loop index.
- **Iterative Binary Search**: `O(1)` - only two index variables.
- **Recursive Binary Search**: `O(log n)` - the recursion call stack.
- **Library Bisect**: `O(1)` - no auxiliary allocation.

### Trade-offs

- **Linear Scan** is the simplest to write and works on unsorted data, but it ignores the sorted structure and fails the required `O(log n)` bound.
- **Iterative Binary Search** gives constant space and full control over the index arithmetic at the cost of slightly more verbose pointer bookkeeping.
- **Recursive Binary Search** reads as a clean divide-and-conquer expression but pays a logarithmic stack cost and adds call overhead.
- **Library Bisect** is the shortest and least bug-prone to write, but it hides the algorithm and requires an explicit presence check to convert an insertion point into a found index.

### When to Use Each

- **Linear Scan**: Only as a baseline or when the array is not sorted; it does not satisfy this problem's logarithmic requirement.
- **Iterative Binary Search**: The default choice for production code and interviews where constant space is valued.
- **Recursive Binary Search**: When the divide-and-conquer structure should be emphasized for readability or teaching.
- **Library Bisect** (Recommended for quick, correct code): When working in Python and a sorted list is already available, and clarity outweighs demonstrating the algorithm.

### Optimization Notes

- The linear scan is the discoverable baseline; the three logarithmic solutions all exploit the sorted order to discard half the candidates per step.
- The hand-written binary searches compute `mid` as `left + (right - left) // 2` to avoid the integer overflow that `(left + right) // 2` can cause in fixed-width integer languages.
- The iterative form is generally preferred over the recursive form in production because it avoids the call-stack growth and associated overhead.
