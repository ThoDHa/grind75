# [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/)

**Easy** | **15 minutes** | **Dynamic Programming**

**Pattern:** [DP 1D Linear](../patterns/dp_1d_linear/intuition.md)

**Practice:** [`practice/climbing_stairs/solution.py`](../../practice/climbing_stairs/solution.py)

You are climbing a staircase. It takes `n` steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

## Examples

### Example 1

**Input:** `n = 2`

**Output:** `2`

**Explanation:** There are two ways to climb to the top.

1. 1 step + 1 step
2. 2 steps

### Example 2

**Input:** `n = 3`

**Output:** `3`

**Explanation:** There are three ways to climb to the top.

1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step

## Constraints

- `1 <= n <= 45`

## Solutions

### Brute Force

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        def climb(step: int) -> int:
            # One empty path reaches step 0, and exactly one way reaches step 1
            if step <= 1:
                return 1

            # The last move was either a single step from step - 1
            # or a double step from step - 2
            return climb(step - 1) + climb(step - 2)

        return climb(n)
```

#### Approach

The most direct idea restates the problem as a recurrence and counts every path by hand. To stand on step `n`, the final move was either a single step from `n - 1` or a double step from `n - 2`, so the count for `n` is the sum of the counts for those two predecessors. Recursing without any caching explores the full tree of choices:

1. If `step` is 0 or 1, return 1, since each of those positions is reached exactly one way (an empty climb for 0, a single move for 1)
2. Otherwise return `climb(step - 1) + climb(step - 2)`, summing the ways the two legal final moves could have arrived
3. Let the recursion fan out into a binary tree of calls, recomputing shared subproblems independently

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

- Each call spawns two more, so the call tree roughly doubles at every level
- The number of nodes grows like the Fibonacci numbers, which is exponential in `n`

##### Space Complexity: `O(n)`

- No auxiliary table is allocated, but the recursion stack reaches depth `n` along the deepest path

#### Key Insights

- Writing the recurrence directly from the problem statement is the simplest, most discoverable formulation
- The same step is recomputed exponentially often, which is exactly the waste the later solutions remove
- This baseline is correct but only practical for small `n`; it makes the case for memoization concrete

### Top-Down Memoization

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        memo = {}

        def climb(step: int) -> int:
            # Base cases: a single empty path reaches step 0,
            # and exactly one way reaches step 1
            if step <= 1:
                return 1
            if step in memo:
                return memo[step]

            # The last move was either a single step from step - 1
            # or a double step from step - 2
            memo[step] = climb(step - 1) + climb(step - 2)
            return memo[step]

        return climb(n)
```

#### Approach

This solution keeps the brute force recurrence but caches each step's result in a hand-rolled dictionary so no subproblem is solved twice:

1. The number of ways to reach step `n` equals the ways to reach `n - 1` (then take a single step) plus the ways to reach `n - 2` (then take a double step)
2. Base cases return 1 for steps 0 and 1, since each has exactly one way to be reached
3. Before recursing, check the `memo` dictionary; the first time a step is computed, store it so later calls return instantly
4. This collapses the exponential call tree into one computation per distinct step

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- Memoization ensures each step from 2 to n is computed exactly once
- Each computation combines two cached values in constant time

##### Space Complexity: `O(n)`

- The cache stores one entry per step, and the recursion stack reaches depth n

#### Key Insights

- This problem follows the Fibonacci sequence pattern, so the recurrence is the Fibonacci recurrence
- A plain dictionary makes the cache explicit, with no library call doing the memoization
- Memoization converts the exponential naive recursion into a linear-time solution
- Top-down recursion expresses the relationship most directly, which makes it a natural step before deriving the iterative versions

### Bottom-Up DP

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 1:
            return 1

        # Create array to store number of ways to reach each step
        dp = [0] * (n + 1)
        dp[0] = dp[1] = 1

        # Fill dp array using recurrence relation
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]

        return dp[n]
```

#### Approach

This solution uses bottom-up dynamic programming with tabulation to solve the climbing stairs problem:

1. We create a DP array where `dp[i]` represents the number of ways to climb to the ith step
2. Base cases: `dp[0] = dp[1] = 1` (there's only one way to reach steps 0 and 1)
3. For steps 2 through n, we apply the recurrence relation: `dp[i] = dp[i-1] + dp[i-2]`
4. This relation captures that to reach step i, we can either:
    - Take a single step from step i-1
    - Take a double step from step i-2

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- We iterate through the array once from 2 to n
- Each iteration involves constant time operations

##### Space Complexity: `O(n)`

- We use an array of size n+1 to store the intermediate results

#### Key Insights

- This problem follows the Fibonacci sequence pattern
- The dynamic programming approach breaks down the problem into simpler subproblems
- By storing results of subproblems, we avoid redundant calculations

### Space-Optimized DP

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 1:
            return 1

        # Initialize first two numbers in the sequence
        prev, curr = 1, 1

        # Calculate subsequent numbers using only two variables
        for i in range(2, n + 1):
            temp = curr
            curr = prev + curr
            prev = temp

        return curr
```

#### Approach

This solution optimizes the space usage of the dynamic programming approach:

1. We observe that at any step, we only need the previous two values in the sequence
2. Instead of using an array to store all intermediate results, we use two variables
3. We iteratively update these variables as we move up the staircase
4. This maintains the same logic as the DP with Tabulation approach but uses O(1) space

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- We still need to iterate through each step from 2 to n once

##### Space Complexity: `O(1)`

- We use only a constant amount of extra space regardless of input size

#### Key Insights

- When a DP solution only depends on a fixed number of previous states, we can optimize space usage
- This approach is particularly useful for large inputs where memory might be a concern
- The solution maintains the elegance of the DP approach while being more efficient

### Closed-Form Formula

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        import math

        # Fibonacci closed form formula (Binet's formula)
        sqrt5 = math.sqrt(5)
        fibn = ((1 + sqrt5) / 2) ** (n + 1) - ((1 - sqrt5) / 2) ** (n + 1)
        return int(fibn / sqrt5)
```

#### Approach

This solution uses the closed-form expression for the Fibonacci sequence (Binet's formula):

1. Since the climbing stairs problem follows the Fibonacci sequence where F(n) = ways to climb n stairs
2. We can use the mathematical closed-form solution: F(n) = (φⁿ - (1-φ)ⁿ)/√5
3. Where φ is the golden ratio (1 + √5)/2

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`

- The calculation is done in constant time regardless of n
- However, for very large n, there might be precision issues

##### Space Complexity: `O(1)`

- Only a constant amount of variables are used

#### Key Insights

- Recognizing the problem follows the Fibonacci sequence unlocks a mathematical solution
- This approach is theoretically the most efficient but may face floating-point precision issues
- It's more of a mathematical curiosity than a practical solution for very large n

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(2^n)` - The uncached call tree doubles at each level, growing exponentially
- **Top-Down Memoization**: `O(n)` - Each step is computed once and cached
- **Bottom-Up DP**: `O(n)` - Linear time to build the DP table
- **Space-Optimized DP**: `O(n)` - Same linear time requirement
- **Closed-Form Formula**: `O(1)` - Constant time calculation

### Space Complexity

- **Brute Force**: `O(n)` - No cache, but the recursion stack reaches depth n
- **Top-Down Memoization**: `O(n)` - Cache holds one entry per step plus a recursion stack of depth n
- **Bottom-Up DP**: `O(n)` - Requires an array of size n+1
- **Space-Optimized DP**: `O(1)` - Uses only a constant amount of extra space
- **Closed-Form Formula**: `O(1)` - Uses only a constant amount of extra space

### Trade-offs

- **Brute Force** maps the recurrence onto the problem statement most directly, but recomputes shared subproblems exponentially often, so it is only viable for small n
- **Top-Down Memoization** mirrors the recurrence most directly and computes only the steps it needs, but carries recursion overhead and stack depth proportional to n
- **Bottom-Up DP** is intuitive and good for educational purposes, but uses more space
- **Space-Optimized DP** provides the best balance of simplicity and efficiency for most cases
- **Closed-Form Formula** is theoretically most efficient but can have numerical precision issues

### When to Use Each

- **Brute Force**: When first deriving the recurrence, or as a teaching baseline that motivates memoization
- **Top-Down Memoization**: When recursive thinking feels most natural or as the first step before deriving an iterative solution
- **Bottom-Up DP**: When teaching DP concepts or when space is not a concern
- **Space-Optimized DP**: In most practical scenarios, efficient and easy to understand
- **Closed-Form Formula**: When absolute performance is critical and n is within the range of floating-point precision

### Optimization Notes

- **Space-Optimized DP is the recommended choice**: it preserves the linear-time clarity of the tabulation approach while collapsing the DP array down to two rolling variables, giving `O(1)` space without sacrificing readability
- The Brute Force is the from-scratch starting point; adding a cache to it is exactly what turns its `O(2^n)` time into the memoized `O(n)`
- Top-Down Memoization reaches the same linear complexity, so prefer it when the recursive framing is clearer, but be mindful of Python's recursion limit for large n (the constraint here caps n at 45, well within bounds)
- A key implementation detail is the use of a `temp` variable when updating `prev` and `curr`: the old `curr` must be saved before it is overwritten, otherwise `prev` would advance incorrectly and break the Fibonacci recurrence
- Avoid reaching for the Closed-Form Formula (Binet's formula) in production: although it is `O(1)`, raising the golden ratio to a power relies on floating-point arithmetic that accumulates rounding error and can return an off-by-one result for larger `n`
- Remember the base-case guard `if n <= 1: return 1` in all approaches; without it the loop never runs and the rolling-variable initialization silently returns the wrong count for `n = 0`
