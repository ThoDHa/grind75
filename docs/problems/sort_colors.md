# [Sort Colors](https://leetcode.com/problems/sort-colors/)

**Medium** | **30 minutes** | **Array, Two Pointers, Sorting**

**Pattern:** [Two Pointers](../patterns/two_pointers/intuition.md)

**Practice:** [`practice/sort_colors/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/sort_colors/solution.py)

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

- **Counting Sort**: `O(n)` - Two separate passes, one to count and one to rebuild
- **Dutch National Flag Algorithm**: `O(n)` - Single pass with each element processed at most twice

### Space Complexity

- **Counting Sort**: `O(1)` - Fixed-size counting array of three elements
- **Dutch National Flag Algorithm**: `O(1)` - Only three pointer variables

### Trade-offs

- The Counting Sort approach is simpler to reason about and verify, at the cost of a second traversal of the array
- The Dutch National Flag algorithm sorts in a single pass but requires careful pointer management to remain correct

### When to Use Each

- **Counting Sort**: When implementation clarity and ease of debugging matter more than minimizing passes
- **Dutch National Flag Algorithm**: When a true one-pass, in-place solution is required (satisfies the follow-up constraint)

### Optimization Notes

- Both solutions exploit the limited value range (only `0`, `1`, `2`) to beat general-purpose `O(n log n)` sorting
- The Dutch National Flag algorithm is the recommended solution because it achieves one pass with constant space
- The critical pitfall in Dutch Flag is advancing `current` after swapping a `2` to the right: the swapped-in element is unexamined, so `current` must stay put
- Counting Sort generalizes cleanly if the number of distinct values grows, whereas Dutch Flag is tailored to three-way partitioning
