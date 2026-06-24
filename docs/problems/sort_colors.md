# [Sort Colors](https://leetcode.com/problems/sort-colors/)

**Medium** | **30 minutes** | **Array, Two Pointers, Sorting**

**Pattern:** [Two Pointers](../patterns/two_pointers/intuition.md)

**Practice:** [`practice/sort_colors/solution.py`](../../practice/sort_colors/solution.py)

Given an array `nums` with `n` objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

We will use the integers `0`, `1`, and `2` to represent the color red, white, and blue, respectively.

You must solve this problem without using the library's sort function.

## Examples

### Example 1

**Input:** nums = `[2,0,2,1,1,0]`

**Output:** `[0,0,1,1,2,2]`

### Example 2

**Input:** nums = `[2,0,1]`

**Output:** `[0,1,2]`

## Constraints

- `n == nums.length`
- `1 <= n <= 300`
- `nums[i]` is either `0`, `1`, or `2`.

## Follow-up

Could you come up with a one-pass algorithm using only constant extra space?

## Solutions

### Selection Sort

```python
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        n = len(nums)
        for i in range(n):
            # Find the smallest color in the unsorted tail
            smallest = i
            for j in range(i + 1, n):
                if nums[j] < nums[smallest]:
                    smallest = j
            # Swap it into place at the sorted boundary
            nums[i], nums[smallest] = nums[smallest], nums[i]
```

#### Approach

The problem forbids the library sort, so the most direct response is to write a sort by hand. Selection sort needs no extra structure and no insight about the values: it just repeatedly finds the minimum of the unsorted region and swaps it to the front. With only `0`, `1`, and `2` present this still produces the correct red-white-blue order because ascending numeric order is exactly the required color order.

1. Treat the prefix before index `i` as already sorted.
2. Scan the unsorted tail `i+1 .. n-1` to find the index of the smallest value.
3. Swap that smallest value into position `i`, growing the sorted prefix by one.
4. Repeat until the whole array is sorted.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

For each of the `n` positions the inner loop scans the remaining tail, giving the quadratic `n + (n-1) + ... + 1` comparisons of any selection sort.

##### Space Complexity: `O(1)`

Sorting happens in place with only a few index variables; no auxiliary array is allocated.

#### Key Insights

- Self-derivable baseline: it solves the problem by literally sorting by hand, using no property of the three-color constraint.
- The ascending integer encoding (`0`, `1`, `2`) means a plain numeric sort already yields the red-white-blue order.
- It is correct but wasteful: it re-scans the tail for every position and ignores that only three distinct values exist.

#### Walkthrough

Let us watch Selection Sort run on Example 1: `nums = [2,0,2,1,1,0]`. The outer loop fixes one position `i` at a time. For each `i` it scans the tail `i+1 .. n-1` to find `smallest`, the index of the minimum value there, then swaps `nums[i]` with `nums[smallest]`. Everything before `i` stays sorted.

Each row shows the state after the swap at that `i`:

| `i` | `smallest` (min in tail) | swap | `nums` after swap |
|-----|--------------------------|------|-------------------|
| `0` | `1` (value `0`) | `nums[0] <-> nums[1]` | `[0,2,2,1,1,0]` |
| `1` | `5` (value `0`) | `nums[1] <-> nums[5]` | `[0,0,2,1,1,2]` |
| `2` | `3` (value `1`) | `nums[2] <-> nums[3]` | `[0,0,1,2,1,2]` |
| `3` | `4` (value `1`) | `nums[3] <-> nums[4]` | `[0,0,1,1,2,2]` |
| `4` | `4` (already min) | `nums[4] <-> nums[4]` | `[0,0,1,1,2,2]` |
| `5` | `5` (last element) | `nums[5] <-> nums[5]` | `[0,0,1,1,2,2]` |

At `i=0` the smallest value in the whole array is the `0` at index `1`, so it swaps to the front. At `i=1` the next smallest is the `0` at index `5`. By `i=4` the tail is already in order, so the remaining swaps are no-ops (`smallest == i`). The array is returned in place as `[0,0,1,1,2,2]`, which matches the expected Output.

### Counting Sort

```python
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Counting sort approach - count occurrences then rebuild array
        """
        # Count occurrences of each color
        count = [0, 0, 0]  # count[0], count[1], count[2]

        # First pass: count all colors
        for num in nums:
            count[num] += 1

        # Second pass: rebuild the array
        index = 0
        for color in range(3):  # 0, 1, 2
            for _ in range(count[color]):
                nums[index] = color
                index += 1
```

#### Approach

A more intuitive two-pass approach that first counts occurrences of each color, then rebuilds the array. While conceptually simpler and easier to implement, it requires two passes through the data.

This solution leverages the constraint that only three distinct values exist, making a specialized counting sort more efficient than general-purpose sorting.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Two separate passes through the array, one to count and one to rebuild.

##### Space Complexity: `O(1)`

Uses a fixed-size counting array of 3 elements regardless of input size.

#### Key Insights

- **Constraint exploitation**: Takes advantage of the limited range of values (only 0, 1, 2) rather than using general sorting
- **Multiple passes for simplicity**: Counting sort uses two passes for simpler, easier-to-verify logic
- **Generalizes cleanly**: Counting sort extends naturally if the number of distinct values grows
- **Easier to debug**: The two-pass structure provides an intuitive implementation that is easy to verify and debug

### Dutch National Flag Algorithm

```python
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Dutch National Flag Algorithm - Three-way partitioning in one pass
        """
        left = 0        # Everything before left is 0
        right = len(nums) - 1  # Everything after right is 2
        current = 0     # Current element being processed

        while current <= right:
            if nums[current] == 0:
                # Move 0 to the left region
                nums[left], nums[current] = nums[current], nums[left]
                left += 1
                current += 1  # Safe to advance since we know nums[left] was processed
            elif nums[current] == 1:
                # 1 is already in correct position, just move forward
                current += 1
            else:  # nums[current] == 2
                # Move 2 to the right region
                nums[current], nums[right] = nums[right], nums[current]
                right -= 1
                # Don't advance current! We need to process the swapped element
```

#### Approach

This is the classic algorithm designed by Edsger Dijkstra using three pointers to partition the array into three regions in a single pass. We maintain `left` (boundary between 0s and 1s), `right` (boundary between 1s and 2s), and `current` (element being examined). The key insight is that when swapping a 2 to the right, we must re-examine the swapped element without advancing `current`.

This solution leverages the constraint that only three distinct values exist, making a specialized partitioning algorithm more efficient than general-purpose sorting.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Single pass through the array with each element processed at most twice.

##### Space Complexity: `O(1)`

Only uses three pointer variables.

#### Key Insights

- **Single-pass efficiency**: Dutch Flag achieves optimal efficiency with one pass, satisfying the follow-up constraint
- **Three-way partitioning**: The algorithm demonstrates elegant three-way partitioning that generalizes to quicksort optimizations
- **Constraint exploitation**: Takes advantage of the limited range of values (only 0, 1, 2) rather than using general sorting
- **Pointer movement strategy**: Careful pointer advancement prevents infinite loops and ensures correctness; when swapping a 2 to the right, `current` must stay put since the swapped-in element is unexamined

## Comparison of Solutions

### Time Complexity

- **Selection Sort**: `O(n^2)` - For every position it rescans the unsorted tail to find the minimum
- **Counting Sort**: `O(n)` - Two separate passes, one to count and one to rebuild
- **Dutch National Flag Algorithm**: `O(n)` - Single pass with each element processed at most twice

### Space Complexity

- **Selection Sort**: `O(1)` - Sorts in place with only index variables
- **Counting Sort**: `O(1)` - Fixed-size counting array of three elements
- **Dutch National Flag Algorithm**: `O(1)` - Only three pointer variables

### Trade-offs

- Selection Sort is the simplest to derive because it sorts by hand and uses no property of the values, but its quadratic comparison count makes it the slowest
- The Counting Sort approach is simpler to reason about and verify than Dutch Flag, at the cost of a second traversal of the array
- The Dutch National Flag algorithm sorts in a single pass but requires careful pointer management to remain correct

### When to Use Each

- **Selection Sort**: Only as a from-scratch baseline; never the right call at scale, but it answers "sort it yourself" with zero cleverness
- **Counting Sort**: When implementation clarity and ease of debugging matter more than minimizing passes
- **Dutch National Flag Algorithm**: When a true one-pass, in-place solution is required (satisfies the follow-up constraint)

### Optimization Notes

- Selection Sort ignores the three-value constraint entirely; both linear solutions exploit the limited value range (only `0`, `1`, `2`) to beat general-purpose `O(n log n)` sorting
- The Dutch National Flag algorithm is the recommended solution because it achieves one pass with constant space
- The critical pitfall in Dutch Flag is advancing `current` after swapping a `2` to the right: the swapped-in element is unexamined, so `current` must stay put
- Counting Sort generalizes cleanly if the number of distinct values grows, whereas Dutch Flag is tailored to three-way partitioning
