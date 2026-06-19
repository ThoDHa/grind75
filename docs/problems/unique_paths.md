# [Unique Paths](https://leetcode.com/problems/unique-paths/)

**Medium** | **20 minutes** | **Math, Dynamic Programming, Combinatorics**

**Pattern:** [Grid DP](../patterns/grid_dp/intuition.md)

**Practice:** [`practice/unique_paths/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/unique_paths/solution.py)

There is a robot on an `m x n` grid. The robot is initially located at the top-left corner (i.e., `grid[0][0]`). The robot tries to move to the bottom-right corner (i.e., `grid[m - 1][n - 1]`). The robot can only move either down or right at any point in time.

Given the two integers `m` and `n`, return the number of possible unique paths that the robot can take to reach the bottom-right corner.

The test cases are generated so that the answer will be less than or equal to `2 * 10^9`.

## Examples

### Example 1

**Input:** `m = 3`, `n = 7`

**Output:** `28`

### Example 2

**Input:** `m = 3`, `n = 2`

**Output:** `3`

**Explanation:** From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
1. Right -> Down -> Down
2. Down -> Down -> Right
3. Down -> Right -> Down

## Constraints

- `1 <= m, n <= 100`

## Solutions

### Bottom-Up DP

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # Create DP table where dp[i][j] = paths to reach cell (i, j)
        dp = [[1] * n for _ in range(m)]

        # Fill the DP table
        for i in range(1, m):
            for j in range(1, n):
                # Paths to current cell = paths from above + paths from left
                dp[i][j] = dp[i-1][j] + dp[i][j-1]

        return dp[m-1][n-1]
```

#### Approach

The key insight is that to reach any cell (i, j), the robot must come from either the cell above (i-1, j) or the cell to the left (i, j-1). Therefore: `paths[i][j] = paths[i-1][j] + paths[i][j-1]`

The base cases are:
- First row: only 1 way to reach each cell (keep moving right)
- First column: only 1 way to reach each cell (keep moving down)

This bottom-up approach fills a full 2D table, mirroring the recurrence directly.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

We fill each cell of the DP table exactly once.

##### Space Complexity: `O(m × n)`

We store the entire 2D DP table.

#### Key Insights

- **Subproblem structure**: The number of paths to any cell depends only on paths to adjacent cells, making this ideal for dynamic programming
- **Boundary conditions**: The first row and column naturally have exactly 1 path each, serving as base cases for the recurrence relation

### Space-Optimized DP

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # Use only one row for space optimization
        dp = [1] * n

        for i in range(1, m):
            for j in range(1, n):
                dp[j] += dp[j-1]

        return dp[n-1]
```

#### Approach

This applies the same recurrence as the 2D DP, but recognizes that calculating the current row only requires the previous row. By updating a single row in place, `dp[j] += dp[j-1]` reuses the old value of `dp[j]` (the cell above) and the freshly updated `dp[j-1]` (the cell to the left), collapsing storage to a single row.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

The same number of cell updates as the 2D DP, just stored in a single row.

##### Space Complexity: `O(n)`

We keep only one row of results.

#### Key Insights

- **Space optimization opportunity**: Since we only need the previous row to calculate the current row, we can reduce space complexity from O(m×n) to O(n)
- **In-place update correctness**: `dp[j] += dp[j-1]` works because the old `dp[j]` represents the cell above and the updated `dp[j-1]` represents the cell to the left

### Combinatorics

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # Total moves needed: (m-1) down + (n-1) right = (m+n-2) total moves
        # Choose (m-1) positions for down moves out of (m+n-2) total positions
        # This equals C(m+n-2, m-1) = C(m+n-2, n-1)

        total_moves = m + n - 2
        down_moves = m - 1

        # Calculate C(total_moves, down_moves) efficiently
        result = 1
        for i in range(down_moves):
            result = result * (total_moves - i) // (i + 1)

        return result
```

#### Approach

From a mathematical perspective, the robot needs to make exactly (m-1) down moves and (n-1) right moves for a total of (m+n-2) moves. The problem reduces to: "In how many ways can we choose (m-1) positions for down moves out of (m+n-2) total positions?" This is the binomial coefficient C(m+n-2, m-1). The loop multiplies before dividing to keep intermediate values integral and avoid overflow.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(min(m, n))`

We compute a single binomial coefficient, iterating over `min(m-1, n-1)` terms.

##### Space Complexity: `O(1)`

We use only a constant number of variables.

#### Key Insights

- **Mathematical elegance**: The combinatorics approach provides the most efficient solution by recognizing this as a "choose k from n" problem
- **Overflow avoidance**: Multiplying before dividing within the loop keeps intermediate values integral

## Comparison of Solutions

### Time Complexity

- **Bottom-Up DP**: `O(m × n)` - Fills every cell of the DP table once
- **Space-Optimized DP**: `O(m × n)` - Same number of cell updates, just stored in a single row
- **Combinatorics**: `O(min(m, n))` - Computes a single binomial coefficient

### Space Complexity

- **Bottom-Up DP**: `O(m × n)` - Stores the entire 2D DP table
- **Space-Optimized DP**: `O(n)` - Keeps only one row of results
- **Combinatorics**: `O(1)` - Uses a constant number of variables

### Trade-offs

- The 2D DP solution is the most readable and mirrors the recurrence directly, but wastes memory storing rows it no longer needs
- The 1D DP solution keeps the same intuitive logic while collapsing storage to a single row, at the cost of slightly less obvious indexing
- The combinatorics solution is the fastest and lightest, but trades away the transparent grid intuition for a mathematical insight

### When to Use Each

- **Bottom-Up DP**: When clarity is paramount or the grid will be extended with obstacles or weights that break the pure combinatorial form
- **Space-Optimized DP**: When the DP structure is still needed but memory is constrained
- **Combinatorics**: When raw speed and minimal space are the priority and the problem stays a clean down/right path count

### Optimization Notes

- The 1D DP works because `dp[j] += dp[j-1]` reuses the old value of `dp[j]` (the cell above) and the freshly updated `dp[j-1]` (the cell to the left)
- The combinatorics solution is the recommended optimum: it multiplies before dividing within the loop to keep intermediate values integral and avoid overflow
- Iterating the binomial coefficient over `min(m-1, n-1)` terms keeps the work minimal regardless of grid orientation
