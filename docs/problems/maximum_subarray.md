# [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/)

**Easy** | **20 minutes** | **Array, Dynamic Programming, Divide and Conquer**

**Pattern:** [Prefix Sum](../patterns/prefix_sum/intuition.md), [DP 1D Linear](../patterns/dp_1d_linear/intuition.md)

**Practice:** [`practice/maximum_subarray/solution.py`](../../practice/maximum_subarray/solution.py)

Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return *its sum*.

A **subarray** is a contiguous part of an array.

## Examples

### Example 1

**Input:** `nums = [-2,1,-3,4,-1,2,1,-5,4]`

**Output:** `6`

**Explanation:** The subarray `[4,-1,2,1]` has the largest sum 6.

### Example 2

**Input:** `nums = [1]`

**Output:** `1`

**Explanation:** The subarray `[1]` has the largest sum 1.

### Example 3

**Input:** `nums = [5,4,-1,7,8]`

**Output:** `23`

**Explanation:** The subarray `[5,4,-1,7,8]` has the largest sum 23.

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

**Follow up:** If you have figured out the `O(n)` solution, try coding another solution using the **divide and conquer approach**, which is more subtle.

## Solutions

### Brute Force

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        n = len(nums)
        best = nums[0]

        for start in range(n):
            # Grow the subarray that begins at `start` one element at a time,
            # carrying the running sum so each new end is constant work.
            current = 0
            for end in range(start, n):
                current += nums[end]
                best = max(best, current)

        return best
```

#### Approach

The most direct idea is to consider every possible contiguous subarray, sum it, and keep the largest sum found. A subarray is fixed by its start and end indices, so two nested loops enumerate all of them.

1. Initialize `best` to `nums[0]` so the answer is valid even when every number is negative.
2. For each start index, reset a `current` running sum to `0`.
3. Sweep `end` from `start` to the array's end, adding `nums[end]` to `current` so it always holds the sum of `nums[start..end]`.
4. Update `best` with the largest sum seen at any `(start, end)` pair.
5. Return `best` after all pairs are examined.

Carrying the running sum across the inner loop avoids re-adding the same prefix for every end, which keeps the work quadratic rather than cubic.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The outer loop fixes each of the `n` start indices, and the inner loop extends to the end of the array, so the total number of `(start, end)` pairs is on the order of `n^2`, each handled in constant time.

##### Space Complexity: `O(1)`

Only the `best` and `current` scalars are tracked, regardless of input size.

#### Key Insights

- Enumerates the entire search space directly, making correctness obvious without any clever observation.
- Reusing the running `current` sum is the one optimization that drops a naive `O(n^3)` re-sum down to `O(n^2)`.
- Seeding `best` with `nums[0]` rather than `0` is what handles the all-negative case correctly.
- Too slow for the upper constraint of `10^5` elements, which motivates the linear approaches below.

#### Walkthrough

Example 1 has 9 elements, which makes 45 `(start, end)` pairs: too many to trace by hand. So this walkthrough uses a smaller array, `nums = [-2, 1, -3, 4]`, whose largest subarray is `[4]` with sum `4`.

We start with `best = nums[0] = -2`. The outer loop fixes each `start`; for each one we reset `current = 0`, then sweep `end` from `start` to the array's end, adding `nums[end]` to `current` (so `current` always holds the sum of `nums[start..end]`) and updating `best` with `max(best, current)`.

Each row below is one `(start, end)` pair: the element just added, the running `current` sum, and `best` after the update.

| `start` | `end` | `nums[end]` | `current` (sum of `nums[start..end]`) | `best` |
| ------- | ----- | ----------- | ------------------------------------- | ------ |
| 0 | 0 | `-2` | `-2` | `-2` |
| 0 | 1 | `1` | `-1` | `-1` |
| 0 | 2 | `-3` | `-4` | `-1` |
| 0 | 3 | `4` | `0` | `0` |
| 1 | 1 | `1` | `1` | `1` |
| 1 | 2 | `-3` | `-2` | `1` |
| 1 | 3 | `4` | `2` | `2` |
| 2 | 2 | `-3` | `-3` | `2` |
| 2 | 3 | `4` | `1` | `2` |
| 3 | 3 | `4` | `4` | `4` |

When `start` moves to a new index, `current` resets to `0` before the first `end` is added, so each row's `current` is the sum of exactly the subarray `nums[start..end]`. The largest `current` ever seen is `4`, from the single-element subarray `[4]` at `start = end = 3`.

After all pairs are examined, the loop returns `best = 4`, which matches the expected sum of the best subarray for `[-2, 1, -3, 4]`.

### Kadane's Algorithm

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        current_sum = nums[0]
        max_sum = nums[0]

        for i in range(1, len(nums)):
            # Extend the previous subarray, or start fresh at nums[i].
            # Starting fresh wins exactly when current_sum is negative.
            current_sum = max(nums[i], current_sum + nums[i])
            max_sum = max(max_sum, current_sum)

        return max_sum
```

#### Approach

Kadane's algorithm scans the array once while tracking two quantities: `current_sum`, the largest sum of any subarray that ends at the current index, and `max_sum`, the largest sum seen anywhere so far.

1. Initialize both `current_sum` and `max_sum` to `nums[0]`, since the answer must contain at least one element.
2. For each subsequent element, decide whether to extend the running subarray or begin a new one at the current element: `current_sum = max(nums[i], current_sum + nums[i])`.
3. Update `max_sum` with the best `current_sum` observed.
4. Return `max_sum` after the single pass.

The decision at step 2 is correct because a subarray ending at index `i` either stands alone (`nums[i]`) or extends the best subarray ending at `i - 1`. Any negative prefix can only hurt, so the algorithm discards it by restarting.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The array is traversed exactly once, performing constant work per element.

##### Space Complexity: `O(1)`

Only two scalar accumulators are maintained regardless of input size.

#### Key Insights

- A subarray ending at `i` is fully described by a single running sum, collapsing the search space to one scan.
- Restarting whenever `current_sum` turns negative is the heart of the algorithm.
- Initializing with `nums[0]` (rather than `0`) handles the all-negative case correctly, returning the least-negative element.

### Dynamic Programming with Explicit Table

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        n = len(nums)
        # dp[i] = largest sum of a subarray ending exactly at index i.
        dp = [0] * n
        dp[0] = nums[0]

        for i in range(1, n):
            dp[i] = max(nums[i], dp[i - 1] + nums[i])

        return max(dp)
```

#### Approach

This formulation makes the dynamic-programming recurrence behind Kadane's algorithm explicit by storing every intermediate state in an array.

1. Define `dp[i]` as the maximum sum of a subarray that ends at index `i`.
2. Set the base case `dp[0] = nums[0]`.
3. Apply the recurrence `dp[i] = max(nums[i], dp[i - 1] + nums[i])` left to right.
4. The answer is `max(dp)`, since the best subarray must end at some index.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Filling the table takes one pass, and the final `max(dp)` takes one more linear pass.

##### Space Complexity: `O(n)`

The explicit `dp` array stores one value per element.

#### Key Insights

- Makes the recurrence visible, which is useful when learning the pattern or when the per-index states are needed later.
- Kadane's algorithm is simply this recurrence with the table compressed to a single rolling variable.
- The base case `dp[0] = nums[0]` again guards the all-negative case.

### Divide and Conquer

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        def max_crossing_sum(left: int, mid: int, right: int) -> int:
            left_sum = float("-inf")
            current = 0
            for i in range(mid, left - 1, -1):
                current += nums[i]
                left_sum = max(left_sum, current)

            right_sum = float("-inf")
            current = 0
            for i in range(mid + 1, right + 1):
                current += nums[i]
                right_sum = max(right_sum, current)

            return left_sum + right_sum

        def divide(left: int, right: int) -> int:
            if left == right:
                return nums[left]

            mid = (left + right) // 2
            left_max = divide(left, mid)
            right_max = divide(mid + 1, right)
            cross_max = max_crossing_sum(left, mid, right)

            return max(left_max, right_max, cross_max)

        return divide(0, len(nums) - 1)
```

#### Approach

The divide-and-conquer solution (requested by the follow-up) splits the array and observes that the maximum subarray falls into exactly one of three categories.

1. Base case: a single element returns its own value.
2. Split at `mid` and recursively solve the left and right halves.
3. Compute the best subarray that crosses `mid` by expanding outward from the midpoint in both directions and summing the two best halves.
4. Return the maximum of the left, right, and crossing results.

The crossing computation is the key piece: the best crossing subarray is forced to include `nums[mid]` and `nums[mid + 1]`, so each side is found greedily by accumulating from the midpoint outward.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The recurrence is `T(n) = 2T(n / 2) + O(n)`, where the `O(n)` crossing scan at each level yields `O(log n)` levels of linear work.

##### Space Complexity: `O(log n)`

The recursion stack reaches a depth proportional to the height of the balanced split.

#### Key Insights

- The three-case decomposition (left, right, crossing) is a reusable divide-and-conquer template.
- Only the crossing case requires explicit work; the halves are handled by recursion.
- It is asymptotically slower than Kadane's, but it illustrates the paradigm and parallelizes naturally across the independent halves.

### Prefix-Sum Minimum

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        best = float("-inf")
        prefix = 0
        min_prefix = 0  # smallest prefix sum strictly before the current index

        for x in nums:
            prefix += x
            best = max(best, prefix - min_prefix)
            min_prefix = min(min_prefix, prefix)

        return best
```

#### Approach

The sum of the subarray `nums[i..j]` equals `prefix[j] - prefix[i - 1]`. To maximize it while ending at index `j`, subtract the smallest prefix sum seen before `j`.

1. Maintain a running `prefix` sum and `min_prefix`, the smallest prefix sum seen at any earlier boundary.
2. At each element, the best subarray ending here is `prefix - min_prefix`; update `best` with it.
3. Update `min_prefix` after using it, so the boundary is always strictly before the current end.
4. Return `best`.

Seeding `min_prefix = 0` represents the empty prefix before the array starts, which lets the subarray begin at index `0`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

A single pass updates the prefix sum and running minimum.

##### Space Complexity: `O(1)`

Only three scalars are tracked.

#### Key Insights

- Recasts the problem as "largest gap between a prefix sum and an earlier minimum prefix sum."
- Equivalent in cost to Kadane's, but the prefix-sum framing generalizes to range-sum variants.
- Updating `min_prefix` after computing `best` enforces the at-least-one-element rule.

### Library One-Liner with `itertools.accumulate`

```python
import itertools


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        return max(itertools.accumulate(nums, lambda acc, x: max(x, acc + x)))
```

#### Approach

`itertools.accumulate` carries Kadane's recurrence as its binary combiner, producing the stream of best-sums-ending-here, and `max` selects the overall best.

1. The accumulator starts at `nums[0]` (the first element passes through unchanged).
2. Each step applies `max(x, acc + x)`, exactly the Kadane decision to extend or restart.
3. `max(...)` over the resulting iterable is the answer.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

`accumulate` yields `n` values, each from a constant-time combiner, and `max` consumes them once.

##### Space Complexity: `O(1)`

`accumulate` is lazy and `max` consumes it as a stream, so no intermediate list is materialized.

#### Key Insights

- A faithful compression of Kadane's algorithm into the standard library's scan primitive.
- Reads concisely, but hides the running-sum logic inside the lambda, which can obscure the core idea.
- Functionally identical in complexity to the hand-written Kadane scan.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - every `(start, end)` pair with a carried running sum.
- **Kadane's Algorithm**: `O(n)` - single linear scan.
- **Dynamic Programming with Explicit Table**: `O(n)` - one pass to fill the table plus one to take the max.
- **Divide and Conquer**: `O(n log n)` - `O(n)` crossing work across `O(log n)` levels.
- **Prefix-Sum Minimum**: `O(n)` - single pass tracking a running minimum prefix.
- **Library One-Liner**: `O(n)` - one accumulate-and-max pass.

### Space Complexity

- **Brute Force**: `O(1)` - two scalars for the running sum and best.
- **Kadane's Algorithm**: `O(1)` - two rolling accumulators.
- **Dynamic Programming with Explicit Table**: `O(n)` - stores one state per element.
- **Divide and Conquer**: `O(log n)` - recursion stack depth.
- **Prefix-Sum Minimum**: `O(1)` - three scalars.
- **Library One-Liner**: `O(1)` - lazy streaming with no intermediate list.

### Trade-offs

- Brute Force gains the simplest, most obviously correct enumeration but is too slow for large inputs.
- Kadane's algorithm gives the best time and space at the cost of a non-obvious restart insight.
- The explicit DP table trades `O(n)` space for clarity and reusable per-index states.
- Divide and conquer trades efficiency for a teachable paradigm and natural parallelism.
- The prefix-sum framing trades nothing in cost while opening the door to range-sum generalizations.
- The library one-liner trades readability of the core logic for brevity.

### When to Use Each

- **Brute Force**: Only as a correctness baseline or for tiny inputs; never for the full constraint.
- **Kadane's Algorithm**: The default choice for interviews and production (recommended).
- **Dynamic Programming with Explicit Table**: When teaching the recurrence or when the intermediate states are needed downstream.
- **Divide and Conquer**: When the follow-up demands it or when parallelizing across halves.
- **Prefix-Sum Minimum**: When the surrounding problem already reasons about prefix sums.
- **Library One-Liner**: When concise, idiomatic Python is preferred and the team knows Kadane's recurrence.

### Optimization Notes

- The brute force already carries a running sum to avoid re-adding prefixes, which is what keeps it `O(n^2)` instead of `O(n^3)`; the linear approaches below collapse it further by reusing the best subarray ending at the previous index.
- Kadane's algorithm and the explicit DP table are the same recurrence; the former simply compresses the table to one rolling variable.
- Initializing accumulators to `nums[0]` (rather than `0`) is what makes the all-negative case correct across the linear-scan variants.
- The divide-and-conquer halves are independent and could be evaluated in parallel for very large arrays.
- All approaches handle all-negative inputs correctly, returning the maximum single element.
