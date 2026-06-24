# [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)

**Hard** | **35 minutes** | **Array, Two Pointers, Dynamic Programming, Stack, Monotonic Stack**

**Pattern:** [Monotonic Stack](../patterns/monotonic_stack/intuition.md)

**Practice:** [`practice/trapping_rain_water/solution.py`](../../practice/trapping_rain_water/solution.py)

Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it can trap after raining.

## Examples

### Example 1

**Input:** `height = [0,1,0,2,1,0,1,3,2,1,2,1]`

**Output:** `6`

**Explanation:** The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.

### Example 2

**Input:** `height = [4,2,0,3,2,5]`

**Output:** `9`

## Constraints

- `n == height.length`
- `1 <= n <= 2 * 10^4`
- `0 <= height[i] <= 3 * 10^4`

## Solutions

### Brute Force

```python
class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        trapped = 0

        for i in range(n):
            # Tallest bar at or to the left of i
            left_max = 0
            for j in range(i + 1):
                left_max = max(left_max, height[j])

            # Tallest bar at or to the right of i
            right_max = 0
            for j in range(i, n):
                right_max = max(right_max, height[j])

            # Water above this bar is bounded by the shorter wall on each side.
            trapped += min(left_max, right_max) - height[i]

        return trapped
```

#### Approach

The most intuitive idea works one bar at a time and asks a simple question: how much
water sits directly above bar `i`? Water can only rest there if taller bars hem it in
on both sides, and it rises to the level of the shorter of those two walls. So for each
bar we find the tallest bar on its left and the tallest on its right, take the smaller of
the two, and subtract the bar's own height.

1. For every index `i`, scan left from the start to find the tallest bar at or before `i`.
2. Scan right to the end to find the tallest bar at or after `i`.
3. Add `min(left_max, right_max) - height[i]` to the running total.

Because `left_max` and `right_max` both include `height[i]` itself, the contribution is
never negative: a bar that is the tallest on one side traps nothing and adds `0`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

For each of the `n` bars we rescan the entire array to recompute both maxima, so the work
is quadratic.

##### Space Complexity: `O(1)`

Only a few scalar accumulators are tracked; no auxiliary array is allocated.

#### Key Insights

- Encodes the core definition directly: trapped water above a bar is
  `min(maxLeft, maxRight) - height[i]`.
- Simple to derive under pressure because it mirrors the physical intuition of walls
  holding water.
- Wasteful: every bar recomputes the same prefix and suffix maxima from scratch, which the
  next approach caches away.

### Prefix and Suffix Maximums

```python
class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        if n == 0:
            return 0

        left_max = [0] * n
        right_max = [0] * n

        left_max[0] = height[0]
        for i in range(1, n):
            left_max[i] = max(left_max[i - 1], height[i])

        right_max[n - 1] = height[n - 1]
        for i in range(n - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], height[i])

        trapped = 0
        for i in range(n):
            trapped += min(left_max[i], right_max[i]) - height[i]

        return trapped
```

#### Approach

This is the dynamic programming formulation: `left_max` and `right_max` are DP tables
where each entry depends on the previous one (`left_max[i] = max(left_max[i-1], height[i])`),
caching the subproblem results that the trapping formula needs. We precompute, for every
index, the tallest bar at or to its left (`left_max`) and at or to its right (`right_max`),
then sum `min(left_max[i], right_max[i]) - height[i]` across all bars.

1. Build `left_max` in a forward sweep.
2. Build `right_max` in a backward sweep.
3. For each bar, the trapped water is `min(left_max[i], right_max[i]) - height[i]`.

It refines the brute force by computing each prefix and suffix maximum once and reusing it,
turning the quadratic rescans into two linear sweeps, at the cost of two auxiliary arrays.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Three linear passes over the array.

##### Space Complexity: `O(n)`

Two arrays of size `n` store the prefix and suffix maxima.

#### Key Insights

- Directly encodes the `min(maxLeft, maxRight) - height` definition, making
  correctness self-evident.
- Decoupling the max computations from the summation makes the logic easy to verify.
- The `O(n)` space is the price for clarity; the two-pointer method removes it.

### Monotonic Stack

```python
class Solution:
    def trap(self, height: List[int]) -> int:
        # Stack holds indices of bars in strictly decreasing height order.
        stack = []
        trapped = 0

        for i, h in enumerate(height):
            # While the current bar is taller than the bar at the top, that top
            # bar forms the floor of a basin bounded by its left neighbor and i.
            while stack and height[stack[-1]] < h:
                floor = stack.pop()

                # No left wall means water spills off the left edge: nothing trapped.
                if not stack:
                    break

                left = stack[-1]
                width = i - left - 1
                # Water height is the shorter of the two walls minus the floor.
                bounded = min(height[left], h) - height[floor]
                trapped += width * bounded

            stack.append(i)

        return trapped
```

#### Approach

Instead of asking how much water sits above each bar, this approach fills water in
horizontal layers between bars. The stack holds indices of bars whose heights are
decreasing from bottom to top, so the top is always the most recent dip.

When a bar taller than the stack top arrives, it can act as a right wall. The bar just
popped becomes the floor of a basin, and the new stack top (if any) is the left wall.
The trapped water for that basin is the width between the two walls times the height of
the shorter wall above the floor.

1. Walk left to right, treating the stack as a record of unresolved dips.
2. While the current bar is taller than the top of the stack, pop the top as a floor.
3. If the stack is now empty there is no left wall, so that water escapes; otherwise add
   `(i - left - 1) * (min(height[left], height[i]) - height[floor])`.
4. Push the current index and continue.

A single bar may settle several layers as it pops successively taller floors, and each
index is pushed and popped at most once.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each index is pushed onto the stack once and popped at most once, so the total work
across the whole scan is linear.

##### Space Complexity: `O(n)`

In the worst case (a strictly decreasing elevation map) every index sits on the stack at
once before any pops occur.

#### Key Insights

- The decreasing-height invariant guarantees that when a taller bar arrives, the popped
  bar is genuinely a local floor with a known left wall.
- Water is accumulated layer by layer between walls rather than column by column, which
  is what makes the per-segment breakdown available if it is ever needed.
- The empty-stack check after a pop is essential: it discards water that would spill off
  the left edge when no left wall exists.

### Two Pointers

```python
class Solution:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0

        left, right = 0, len(height) - 1
        left_max, right_max = height[left], height[right]
        trapped = 0

        while left < right:
            # Advance the side with the smaller running max. The water level at
            # that pointer is fully determined by its own side's max.
            if left_max <= right_max:
                left += 1
                left_max = max(left_max, height[left])
                trapped += left_max - height[left]
            else:
                right -= 1
                right_max = max(right_max, height[right])
                trapped += right_max - height[right]

        return trapped
```

#### Approach

The water sitting above any bar `i` equals `min(maxLeft[i], maxRight[i]) - height[i]`,
where `maxLeft` and `maxRight` are the tallest bars to the left and right. The
challenge is computing that minimum without storing both prefix arrays.

The two-pointer method exploits a key observation: if `left_max <= right_max`, then
the water level at the left pointer is bounded by `left_max`, regardless of what taller
bars might lie further right, because we already know some bar on the right is at least
`right_max >= left_max`. So we can safely settle the left pointer's water using only
`left_max`, and symmetrically for the right.

1. Place pointers at both ends and seed `left_max` / `right_max` with the endpoints.
2. Repeatedly move the pointer on the side with the smaller running max inward.
3. Update that side's running max, then add `running_max - height` at the new
   position to the total.
4. Stop when the pointers meet.

This computes the correct trapped water in a single pass with constant extra memory.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each pointer moves inward at most `n` times total, so we touch every bar once.

##### Space Complexity: `O(1)`

Only a fixed number of scalars are tracked regardless of input size.

#### Key Insights

- The water above a bar depends on the minimum of the max heights to its left and
  right; the two-pointer trick obtains that minimum implicitly.
- Always moving the smaller-max side is what makes the local decision provably safe.
- No auxiliary arrays are needed, beating the prefix/suffix approach on space.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - every bar rescans the whole array for both maxima.
- **Prefix and Suffix Maximums**: `O(n)` - three linear passes.
- **Monotonic Stack**: `O(n)` - each index is pushed and popped at most once.
- **Two Pointers**: `O(n)` - single inward sweep.

### Space Complexity

- **Brute Force**: `O(1)` - only scalar accumulators.
- **Prefix and Suffix Maximums**: `O(n)` - two precomputed arrays.
- **Monotonic Stack**: `O(n)` - the stack can hold every index for a decreasing map.
- **Two Pointers**: `O(1)` - a handful of scalars.

### Trade-offs

- The Brute Force approach is the easiest to derive and uses no extra space, but its
  quadratic rescans make it too slow for the upper constraint of `2 * 10^4` bars.
- The Prefix and Suffix Maximums approach trades `O(n)` space for a transparent, formula-driven implementation
  that caches the brute force's repeated maxima into two linear sweeps.
- The Monotonic Stack approach also uses `O(n)` space but fills water in horizontal
  layers, which is the natural fit when a per-segment breakdown is wanted.
- The Two Pointers approach achieves optimal constant space but relies on the subtler invariant
  that the smaller running max bounds its side's water level.

### When to Use Each

- **Brute Force**: As a first correctness check or to derive the trapping formula before
  optimizing; not viable at full input size.
- **Prefix and Suffix Maximums**: When clarity matters most or as a stepping
  stone to first establish correctness before optimizing.
- **Monotonic Stack**: When a layer-by-layer or per-segment view of the trapped water
  is useful, or to practice the broader monotonic-stack pattern.
- **Two Pointers**: When memory is constrained or the interviewer asks
  for the optimal space solution.

### Optimization Notes

- The Brute Force recomputes the same prefix and suffix maxima for every bar; the Prefix
  and Suffix Maximums approach caches them, dropping the time from `O(n^2)` to `O(n)`.
- The three linear approaches differ only in space and in how the trapped water is
  accounted for (per column, per layer, or implicitly).
- The Prefix and Suffix Maximums and Two Pointers solutions short-circuit on an empty
  input to avoid indexing errors, while the Monotonic Stack handles it naturally because
  the loop body never runs.
