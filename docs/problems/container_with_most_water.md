# [Container With Most Water](https://leetcode.com/problems/container-with-most-water/)

**Medium** | **15 minutes** | **Array**

**Pattern:** [Two Pointers](../patterns/two_pointers/intuition.md)

**Practice:** [`practice/container_with_most_water/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/container_with_most_water/solution.py)

You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i`th line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

**Note:** You may not slant the container.

## Examples

**Example 1:**

![Container Example](./assets/container_with_most_water_example1.jpg)

```
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.
```

**Example 2:**

```
Input: height = [1,1]
Output: 1
```

## Constraints

- `n == height.length`
- `2 <= n <= 10^5`
- `0 <= height[i] <= 10^4`

## Solutions

### Brute Force

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        n = len(height)
        max_area = 0

        # Try every pair of lines as the container walls
        for i in range(n):
            for j in range(i + 1, n):
                # Water level is capped by the shorter wall
                width = j - i
                current_height = min(height[i], height[j])
                max_area = max(max_area, width * current_height)

        return max_area
```

#### Approach

The most direct way to solve this is to consider every possible pair of lines as
the two walls of the container. For each pair `(i, j)`, the amount of water it
holds is limited by the shorter of the two lines, multiplied by the horizontal
distance between them.

1. Iterate over every starting line `i`.
2. For each `i`, iterate over every later line `j`.
3. Compute the area as `min(height[i], height[j]) * (j - i)`.
4. Track the maximum area seen across all pairs.

This examines all `n * (n - 1) / 2` pairs, guaranteeing the optimum is found, but
the quadratic work makes it impractical for large inputs.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The nested loops evaluate every pair of lines, which grows quadratically with the
number of lines.

##### Space Complexity: `O(1)`

Only a few scalar variables are used regardless of input size.

#### Key Insights

- Provides a correct baseline by exhaustively checking every container
- The limiting wall is always the shorter line, so the height term is a `min`
- The quadratic pair count is what the two-pointer approach later eliminates

### Two Pointers

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        max_area = 0

        while left < right:
            # Calculate current area
            width = right - left
            current_height = min(height[left], height[right])
            current_area = width * current_height

            # Update maximum area if current is larger
            max_area = max(max_area, current_area)

            # Move the pointer with smaller height inward
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_area
```

#### Approach

This problem uses the **two-pointer technique** with a key optimization insight. The container's water capacity is determined by the shorter of the two lines and the distance between them (area = width × height).

The algorithm works as follows:

1. **Start with maximum width**: Place pointers at the far ends (leftmost and rightmost positions) to begin with the maximum possible width.

2. **Calculate current area**: For each pair of lines, compute the area as `width × min(height[left], height[right])`.

3. **Greedy pointer movement**: Always move the pointer pointing to the shorter line inward. This is the key insight:
    - Moving the taller line inward can only decrease width while keeping the limiting height the same (or worse)
    - Moving the shorter line inward decreases width but gives us a chance to find a taller line that might compensate for the lost width

4. **Track maximum**: Keep track of the maximum area encountered during the process.

The greedy choice is optimal because we're systematically exploring all potentially better configurations while pruning impossible ones.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We make a single pass through the array using two pointers that move toward each other. Each element is visited at most once, making this a linear time algorithm.

##### Space Complexity: `O(1)`

The algorithm uses only a constant amount of extra space for variables (`left`, `right`, `max_area`, `current_area`, etc.), regardless of the input size.

#### Key Insights

- **Two-pointer optimization**: Starting from the widest possible container and systematically narrowing based on height constraints ensures we don't miss the optimal solution
- **Greedy choice correctness**: Moving the shorter line is always the right choice because keeping it would only yield worse results as we decrease width
- **No need to check all pairs**: The naive O(n²) approach of checking every pair is unnecessary due to the pruning property of the two-pointer technique
- **Geometric intuition**: We're finding the rectangle with maximum area under the constraint that one side must touch the x-axis and the other two sides are limited by the given heights

### Two Pointers with Skip Optimization

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        max_area = 0

        while left < right:
            # Limiting wall and current area
            current_height = min(height[left], height[right])
            max_area = max(max_area, current_height * (right - left))

            # Advance past every line no taller than the limiting wall:
            # those positions can only shrink width without raising the cap
            if height[left] < height[right]:
                while left < right and height[left] <= current_height:
                    left += 1
            else:
                while left < right and height[right] <= current_height:
                    right -= 1

        return max_area
```

#### Approach

This is the same two-pointer scan, refined with a pruning observation. After
processing a pair, the limiting wall is the shorter of the two. Any line on that
side whose height is less than or equal to the current limiting height cannot
improve the answer: moving inward reduces the width while the height stays capped
at the same value or lower.

1. Start with the pointers at the two ends and record the area of that pair.
2. Identify the shorter wall, which is the current limiting height.
3. Instead of advancing the shorter side by a single step, skip every consecutive
   line on that side that is no taller than the limiting height.
4. Repeat until the pointers meet.

The result is identical to the plain two-pointer scan; the inner skip loops simply
collapse runs of useless positions in one move.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each pointer only ever moves inward, and the inner skip loops advance the same
pointers. Across the whole run every index is visited at most once, so the total
work remains linear.

##### Space Complexity: `O(1)`

Only the two pointers and a couple of scalar variables are stored, independent of
input size.

#### Key Insights

- **Pruning runs of short lines**: A line no taller than the current limiting wall
  can never beat the area already recorded, so it is safe to skip past it
- **Same asymptotic bound, smaller constant**: The skip loops do not change the
  `O(n)` complexity but can reduce the number of area computations on inputs with
  long plateaus or many short lines
- **Correctness preserved**: Because skipped lines are provably non-improving, the
  optimized scan returns exactly the same maximum as the plain two-pointer version

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - Evaluates every pair of lines
- **Two Pointers**: `O(n)` - Single pass with two converging pointers
- **Two Pointers with Skip Optimization**: `O(n)` - Same single pass, with skip loops that only ever advance the pointers inward

### Space Complexity

- **Brute Force**: `O(1)` - Only scalar tracking variables
- **Two Pointers**: `O(1)` - Only scalar tracking variables
- **Two Pointers with Skip Optimization**: `O(1)` - Only the two pointers and scalar variables

### Trade-offs

- Brute force is trivial to reason about and obviously correct, but its quadratic time makes it unusable for the upper constraint of 10^5 lines
- Two pointers is dramatically faster, at the cost of needing the greedy-movement insight to see why it never misses the optimal container
- The skip-optimized variant adds a small amount of code in exchange for fewer area computations on inputs with long runs of short lines, while keeping the same `O(n)` bound

### When to Use Each

- **Brute Force**: For building intuition or verifying the optimized solution on small inputs
- **Two Pointers**: For any real use, especially under the given constraints where quadratic time would time out
- **Two Pointers with Skip Optimization**: When a slightly lower constant factor matters on inputs with many non-improving lines, and the extra inner loops are acceptable

### Optimization Notes

- The leap from brute force to two pointers comes from the observation that moving the taller wall can never improve the area, so only the shorter wall's pointer should advance
- The skip optimization extends that observation: any line no taller than the current limiting wall is non-improving, so consecutive such lines can be skipped in one move rather than one step at a time
- All three approaches use `O(1)` space, so the entire gain is in time, not memory
