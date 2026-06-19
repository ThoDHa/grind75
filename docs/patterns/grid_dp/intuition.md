# Grid DP: Pattern Intuition Guide

> *"A grid is a staircase with two directions. Every cell's answer is built from the cells you already solved."*

---

## The Situation That Calls for Grid DP

Imagine you're standing in the top-left corner of a city laid out as a perfect grid of streets. You want to reach the bottom-right corner, but you may only walk **right** or **down**. How many distinct routes can you take?

The brute force approach: enumerate every possible sequence of moves. But the number of routes explodes combinatorially as the grid grows.

The DP insight: **The number of ways to reach a given intersection depends only on the intersection directly above it and the one directly to its left.** If you know those two counts, you just add them up.

This is the essence of Grid DP. It is the same idea as the DP 1D Linear guide, raised one dimension higher: **build the answer from smaller subproblems, but now the subproblems live in two dimensions instead of one.** Where 1D DP marched along a line, Grid DP fills a table.

You reach for Grid DP when you see a 2D grid or matrix, movement restricted to a few directions (usually right and down), and a goal of either **counting paths** or **optimizing a path cost** (minimum or maximum).

---

## The Core Insight

Every cell `dp[i][j]` is computed from neighbors that have **already been solved**. For right/down movement, those neighbors are the cell **above** (`dp[i-1][j]`) and the cell **to the left** (`dp[i][j-1]`).

The crucial discipline is **fill order**. You must compute cells in an order that respects these dependencies: a cell may only be filled after the cells it depends on. Filling **row by row, left to right** guarantees that when you arrive at `dp[i][j]`, both the cell above and the cell to the left are ready.

```
1. DEFINE STATE: What does dp[i][j] represent for the subgrid ending at (i, j)?
2. WRITE RECURRENCE: How does dp[i][j] combine its neighbors?
3. SET BASE CASES: Fill the first row and first column directly.
4. CHOOSE FILL ORDER: Row by row, left to right, so dependencies are ready.
5. FIND ANSWER: Usually the bottom-right cell, dp[m-1][n-1].
6. OPTIMIZE SPACE: Collapse the 2D table to a single rolling row.
```

---

## Three Mental Models

### Model 1: The Filled Table

Picture the grid as a spreadsheet you fill in cell by cell. Each cell **aggregates its dependencies**: it sums them (for counting) or takes the best of them plus its own value (for optimizing). The first row and first column are the boundary, seeded with base values. Every interior cell is a small combination of two already-known neighbors.

```
+---+---+---+---+
| 1 | 1 | 1 | 1 |   ← first row: only one path (all rights)
+---+---+---+---+
| 1 | 2 | 3 | 4 |
+---+---+---+---+
| 1 | 3 | 6 |10 |
+---+---+---+---+
```

The answer accumulates in the bottom-right.

### Model 2: The Recurrence

For **Unique Paths** (counting routes), each interior cell sums the two ways to arrive:

```python
dp[i][j] = dp[i-1][j] + dp[i][j-1]
# first row and first column = 1 (one straight-line path)
```

For **minimum path cost**, you instead take the cheaper neighbor and add the current cell's cost:

```python
dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
```

For **maximum**, swap `min` for `max`. The shape is always the same: combine the already-computed neighbors, then fold in the current cell.

### Model 3: Space Optimization (Rolling Row)

Notice the recurrence only ever looks at the **current row** and the **row directly above**. You never need rows further back. So you can collapse the full `m × n` table into a **single 1D row** that you overwrite in place.

```python
# Unique Paths with O(n) space
dp = [1] * n            # represents the first row
for i in range(1, m):
    for j in range(1, n):
        dp[j] += dp[j-1]  # dp[j] is "above", dp[j-1] is "left"
return dp[-1]
```

When you read `dp[j]` before overwriting it, it still holds the value from the **previous row** (the cell above). After the `+=`, it holds the **current row** value. `dp[j-1]` was already updated this pass, so it is the cell to the left. One array does the work of the whole table.

---

## Pattern Recognition Signals

When you see these phrases, think **Grid DP**.

### Signal: "Grid" or "Matrix"
> *"You are given an m x n grid..."*
> *"Starting at the top-left of a matrix..."*

**Action**: Set up a 2D table indexed by row and column.

### Signal: "Move only right or down"
> *"You can only move down or right at any point in time"*
> *"Restricted to moving toward the bottom-right"*

**Action**: Each cell depends on the cell above and the cell to the left. Fill row by row.

### Signal: "Count the number of ways"
> *"How many unique paths are there?"*
> *"In how many ways can you reach the corner?"*

**Action**: Additive recurrence, `dp[i][j] = dp[i-1][j] + dp[i][j-1]`.

### Signal: "Minimum or maximum cost path"
> *"Find a path that minimizes the sum of values"*
> *"Maximize the gold collected along the way"*

**Action**: Optimizing recurrence, `dp[i][j] = grid[i][j] + best(dp[i-1][j], dp[i][j-1])`.

---

## A Worked Trace: Unique Paths on a 3×3 Grid

Let's count the monotone lattice paths from the top-left to the bottom-right of a 3×3 grid, moving only right or down.

**Step 1: Seed the base cases.** There is exactly one path along the top row (keep moving right) and one path down the left column (keep moving down). Fill both with 1.

```
+---+---+---+
| 1 | 1 | 1 |
+---+---+---+
| 1 | . | . |
+---+---+---+
| 1 | . | . |
+---+---+---+
```

**Step 2: Fill `dp[1][1]`** = above + left = `1 + 1 = 2`.

```
+---+---+---+
| 1 | 1 | 1 |
+---+---+---+
| 1 | 2 | . |
+---+---+---+
| 1 | . | . |
+---+---+---+
```

**Step 3: Fill `dp[1][2]`** = above (1) + left (2) = `3`. Then drop to the next row.

```
+---+---+---+
| 1 | 1 | 1 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
| 1 | . | . |
+---+---+---+
```

**Step 4: Fill `dp[2][1]`** = above (2) + left (1) = `3`, then `dp[2][2]` = above (3) + left (3) = `6`.

```
+---+---+---+
| 1 | 1 | 1 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
| 1 | 3 | 6 |
+---+---+---+
```

The values propagate diagonally toward the corner, each one a sum of the two that feed it. The answer is the bottom-right cell: **6 unique paths**.

---

## Common Pitfalls

### Pitfall 1: Wrong Base Cases for the First Row and Column
**Problem**: The recurrence `dp[i-1][j] + dp[i][j-1]` reads out of bounds at the top edge and left edge.

```python
# Wrong: the interior recurrence has no valid "above" on row 0
dp[0][j] = dp[-1][j] + dp[0][j-1]   # ERROR: dp[-1] is invalid

# Right: seed the boundary directly before the main loop
for j in range(n): dp[0][j] = 1   # only rights
for i in range(m): dp[i][0] = 1   # only downs
```

**Solution**: Handle the first row and first column as base cases, then start the main loops at index 1.

### Pitfall 2: Iterating in the Wrong Order
**Problem**: Filling cells before their dependencies are ready (for example, iterating columns-then-rows when the cell above is not yet computed).

**Solution**: Match the loop order to the dependencies. For right/down movement, outer loop over rows, inner loop over columns, both increasing.

### Pitfall 3: Off-by-One on Dimensions
**Problem**: Confusing `m` (rows) with `n` (columns), or indexing `dp[n][m]` instead of `dp[m][n]`.

**Solution**: Pin down a convention early: `m` rows, `n` columns, `dp` sized `m × n`, answer at `dp[m-1][n-1]`. Trace a tiny grid by hand to confirm.

### Pitfall 4: Applying the 1D Rolling Optimization When It Isn't Valid
**Problem**: Collapsing to a single row when the recurrence depends on more than the previous row, or when you must reconstruct the actual path.

**Solution**: The rolling-row trick is valid only when each cell depends solely on the current row and the one directly above. If you need to recover the path itself, or the recurrence reaches further back, keep the full 2D table.

---

## Practice Progression

The canonical entry point in the Grind75 set is **Unique Paths**, which asks you to count the monotone lattice paths across a grid using right-and-down moves. It is the purest expression of the additive recurrence and the ideal place to build the table-filling instinct.

From there, the same machinery extends naturally to optimization variants. **Minimum Path Sum** swaps the additive recurrence for a `min` over the two neighbors plus the current cell. **Edit Distance** generalizes the idea further: the grid is indexed by positions in two strings, and each cell combines its neighbors to express insertions, deletions, and substitutions. All three are the same skeleton, differing only in what each cell aggregates.

---

## The Unifying Principle

Grid DP is **1D Linear DP with a second axis**. The promise is unchanged: if you know the best (or the count) for smaller subproblems, you can combine them to solve the current one.

The two properties that made 1D DP work still hold. **Optimal substructure**: the answer for a cell is built from the answers of its neighbors. **Overlapping subproblems**: the same interior cells feed many paths, so you compute each exactly once and reuse it.

Fill the table in dependency order, let each cell aggregate the neighbors above and to the left, and read the answer out of the corner.

*"Solve every cell once. Build the corner from the cells you already know."*
