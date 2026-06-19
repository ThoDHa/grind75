# [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/)

**Hard** | **60 minutes** | **Array, Stack, Monotonic Stack**

**Pattern:** [Monotonic Stack](../patterns/monotonic_stack/intuition.md)

**Practice:** [`practice/largest_rectangle_in_histogram/solution.py`](../../practice/largest_rectangle_in_histogram/solution.py)

Given an array of integers `heights` representing the histogram's bar height where the width of each bar is `1`, return the area of the largest rectangle in the histogram.

## Examples

### Example 1

![Histogram Example 1](assets/largest_rectangle_in_histogram_example1.jpg)

**Input:** `heights = [2,1,5,6,2,3]`

**Output:** `10`

**Explanation:** The above is a histogram where width of each bar is `1`.
The largest rectangle is shown in the red area, which has an area = `10` units.

### Example 2

![Histogram Example 2](assets/largest_rectangle_in_histogram_example2.jpg)

**Input:** `heights = [2,4]`

**Output:** `4`

## Constraints

- `1 <= heights.length <= 10^5`
- `0 <= heights[i] <= 10^4`

## Solutions

### Brute Force over All Rectangles

```python
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        max_area = 0
        n = len(heights)

        for i in range(n):
            # Treat bar i as the limiting (shortest) bar of the rectangle
            current_height = heights[i]

            # Extend left while neighbors are at least as tall
            left = i
            while left > 0 and heights[left - 1] >= current_height:
                left -= 1

            # Extend right while neighbors are at least as tall
            right = i
            while right < n - 1 and heights[right + 1] >= current_height:
                right += 1

            width = right - left + 1
            max_area = max(max_area, current_height * width)

        return max_area
```

#### Approach

This solution considers each bar as the **limiting height** of a rectangle and extends as far left and right as possible while every bar in the span remains at least that tall. It directly implements the rectangle definition.

1. For each bar `i`, fix its height as the rectangle's ceiling.
2. Walk left until a strictly shorter bar blocks expansion.
3. Walk right until a strictly shorter bar blocks expansion.
4. The area is `heights[i] * width`; keep the running maximum.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

For each bar, we potentially scan the entire array in both directions, giving `n` bars times `O(n)` expansion.

##### Space Complexity: `O(1)`

Uses only a constant amount of extra space.

#### Key Insights

- Every maximal rectangle is bounded by some bar acting as its shortest member, so iterating over candidate limiting bars covers all rectangles.
- The expansion stops at the first strictly shorter neighbor on each side, which defines the rectangle's natural left and right walls.
- Simple to reason about but quadratic, since adjacent bars of equal height force repeated re-scanning of the same span.

### Optimized Brute Force

```python
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        max_area = 0
        n = len(heights)

        for i in range(n):
            # Track the minimum height as the rectangle grows rightward
            min_height = heights[i]

            for j in range(i, n):
                min_height = min(min_height, heights[j])
                width = j - i + 1
                max_area = max(max_area, min_height * width)

        return max_area
```

#### Approach

This **brute force solution** considers every contiguous subarray `[i, j]` and computes the area of the largest rectangle it can support. For each starting position `i`, it expands rightward while tracking the minimum height encountered, since the minimum height bounds the rectangle over that span.

1. Fix a left boundary `i`.
2. Extend the right boundary `j` one bar at a time.
3. Update `min_height` to the smallest bar in `[i, j]`.
4. The candidate area is `min_height * (j - i + 1)`; keep the running maximum.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Nested loops enumerate all `O(n²)` subarrays, with constant work per subarray thanks to the incrementally maintained minimum.

##### Space Complexity: `O(1)`

Uses only a constant amount of extra space.

#### Key Insights

- Maintaining `min_height` incrementally avoids recomputing the minimum over each subarray, keeping per-subarray work constant.
- Enumerating all subarrays guarantees correctness because the optimal rectangle corresponds to some span with its minimum bar as the ceiling.
- It is more uniform than the expansion-based brute force but still quadratic and impractical for large inputs.

### Divide and Conquer

```python
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        def calculate_area(start: int, end: int) -> int:
            if start > end:
                return 0

            # The shortest bar in the range is the only one that can span it fully
            min_idx = start
            for i in range(start, end + 1):
                if heights[i] < heights[min_idx]:
                    min_idx = i

            area_with_min = heights[min_idx] * (end - start + 1)
            left_area = calculate_area(start, min_idx - 1)
            right_area = calculate_area(min_idx + 1, end)

            return max(area_with_min, left_area, right_area)

        if not heights:
            return 0

        return calculate_area(0, len(heights) - 1)
```

#### Approach

This solution uses **divide and conquer** anchored on the minimum height in the current range. The largest rectangle either uses the minimum bar (spanning the whole range), lies entirely to the left of it, or lies entirely to the right of it.

1. Find the index of the minimum bar in `[start, end]`.
2. Compute the area of the rectangle that uses that bar across the full range.
3. Recurse on the left segment and the right segment.
4. Return the maximum of the three candidates.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)` average, `O(n²)` worst case

The average case occurs when the minimum element roughly halves the range at each level. The worst case occurs on a sorted array, where each split peels off a single element and the linear minimum scan repeats.

##### Space Complexity: `O(log n)` average, `O(n)` worst case

Recursion depth tracks how balanced the splits are, from logarithmic in the balanced case to linear on sorted input.

#### Key Insights

- The minimum bar in a range is the only bar that can support a rectangle spanning that entire range, which justifies the three-way split.
- Balance depends entirely on input shape, so the technique degrades to `O(n²)` on monotonic data where the stack approach stays linear.
- It avoids auxiliary boundary arrays but pays a recurring linear scan to locate each minimum.

### Monotonic Stack

```python
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        stack = []  # indices of bars in increasing-height order
        max_area = 0
        n = len(heights)

        for i in range(n):
            # Current bar is the right boundary for every taller bar on the stack
            while stack and heights[stack[-1]] > heights[i]:
                height = heights[stack.pop()]
                # Left boundary is the new stack top; width excludes both walls
                width = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, height * width)
            stack.append(i)

        # Flush remaining bars: their right boundary is the end of the histogram
        while stack:
            height = heights[stack.pop()]
            width = n if not stack else n - stack[-1] - 1
            max_area = max(max_area, height * width)

        return max_area
```

#### Approach

This solution uses a **monotonic stack** of indices kept in increasing height order. For each bar we need the first shorter bar to its left and right; those define how wide a rectangle of that bar's height can be. The stack resolves both boundaries in a single pass.

1. Iterate over the bars, maintaining a stack whose heights increase from bottom to top.
2. When the current bar is shorter than the stack top, pop it: the current index is its right boundary and the new stack top is its left boundary.
3. Compute the popped bar's rectangle width as `i - stack[-1] - 1`, or `i` when the stack empties.
4. After the loop, flush the remaining bars, whose right boundary is the end of the histogram.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each index is pushed and popped at most once, so the total work is linear despite the inner `while` loop.

##### Space Complexity: `O(n)`

In the worst case of strictly increasing heights, the stack holds every index before any pop occurs.

#### Key Insights

- The stack invariant (increasing heights) guarantees that when a bar is popped, the bar immediately below it is its nearest shorter bar on the left.
- The width formula `i - stack[-1] - 1` is the crux: it spans from just past the left boundary to just before the right boundary, and collapses to `i` when no left boundary remains.
- Forgetting to flush the stack after the main loop is the classic bug, since those bars never meet a shorter bar on the right and must extend to the array end.

## Comparison of Solutions

### Time Complexity

- **Brute Force over All Rectangles**: `O(n²)` - Quadratic time
- **Optimized Brute Force**: `O(n²)` - Quadratic time
- **Divide and Conquer**: `O(n log n)` average, `O(n²)` worst case
- **Monotonic Stack**: `O(n)` - Optimal linear time

### Space Complexity

- **Brute Force over All Rectangles**: `O(1)` - Constant space
- **Optimized Brute Force**: `O(1)` - Constant space
- **Divide and Conquer**: `O(log n)` average - Recursion stack
- **Monotonic Stack**: `O(n)` - Stack storage

### Trade-offs

- **Brute Force over All Rectangles**: Poor time efficiency but excellent space efficiency. Implementation complexity is low and conceptual difficulty is very low. Suitable for learning only in an interview setting.
- **Optimized Brute Force**: Poor time efficiency but excellent space efficiency. Implementation complexity is low and conceptual difficulty is low. Suitable for learning only in an interview setting.
- **Divide and Conquer**: Good time efficiency in the average case and excellent space efficiency in the average case. Implementation complexity is medium and conceptual difficulty is medium. Acceptable as an interview answer.
- **Monotonic Stack**: Optimal time efficiency with good space efficiency. Implementation complexity is high and conceptual difficulty is high. This is the most preferred solution in interviews.

### When to Use Each

- **Brute Force over All Rectangles**: Only for learning the basic problem definition
- **Optimized Brute Force**: For understanding the problem structure and building intuition
- **Divide and Conquer**: When recursion is preferred or as a stepping stone to the optimal solution
- **Monotonic Stack**: Best solution for production and interviews: optimal time complexity

### Optimization Notes

- The **Monotonic Stack** solution is the recommended approach: it achieves optimal `O(n)` time by guaranteeing each bar is pushed and popped at most once.
- The critical implementation detail is the width calculation when popping: the width spans from the next smaller bar on the left (the new stack top after popping) to the current bar on the right, computed as `i - stack[-1] - 1`, or `i` when the stack becomes empty.
- A common pitfall is forgetting to process the bars remaining on the stack after the main loop ends. These bars have no smaller bar to their right, so their width extends to the end of the histogram.
- This problem is the classic example of monotonic stack applications, and the same "next greater/smaller element" technique generalizes to many related problems. Edge cases such as empty arrays, single elements, and arrays containing zeros require careful handling across all approaches.
