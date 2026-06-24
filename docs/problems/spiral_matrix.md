# [Spiral Matrix](https://leetcode.com/problems/spiral-matrix/)

**Medium** | **30 minutes** | **Array, Matrix, Simulation**

**Pattern:** [Simulation](../patterns/simulation/intuition.md)

**Practice:** [`practice/spiral_matrix/solution.py`](../../practice/spiral_matrix/solution.py)

Given an `m x n` matrix, return all elements of the `matrix` in spiral order.

## Examples

### Example 1

**Input:** matrix = `[[1,2,3],[4,5,6],[7,8,9]]`

**Output:** `[1,2,3,6,9,8,7,4,5]`

### Example 2

**Input:** matrix = `[[1,2,3,4],[5,6,7,8],[9,10,11,12]]`

**Output:** `[1,2,3,4,8,12,11,10,9,5,6,7]`

## Constraints

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 10`
- `-100 <= matrix[i][j] <= 100`

## Solutions

### Direction Vector Walk

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """
        Use direction vectors and turn when hitting boundaries or visited cells
        """
        if not matrix or not matrix[0]:
            return []

        m, n = len(matrix), len(matrix[0])
        result = []
        visited = [[False] * n for _ in range(m)]

        # Direction vectors: right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        direction_idx = 0

        row, col = 0, 0

        for _ in range(m * n):
            result.append(matrix[row][col])
            visited[row][col] = True

            # Calculate next position
            dr, dc = directions[direction_idx]
            next_row, next_col = row + dr, col + dc

            # Check if we need to turn (hit boundary or visited cell)
            if (next_row < 0 or next_row >= m or
                next_col < 0 or next_col >= n or
                visited[next_row][next_col]):
                # Turn clockwise to next direction
                direction_idx = (direction_idx + 1) % 4
                dr, dc = directions[direction_idx]
                next_row, next_col = row + dr, col + dc

            row, col = next_row, next_col

        return result
```

#### Approach

This is the most intuitive way to discover the answer from scratch: literally walk the spiral the way a person would trace it by hand. Carry a current direction drawn from the ordered list `right, down, left, up`, mark each cell as visited, then peek at the next cell in the current direction. If that step would leave the grid or land on a cell already visited, rotate the direction index clockwise by one and step that way instead. After exactly `m × n` steps every cell has been emitted in spiral order.

1. Allocate a `visited` grid and start at the top-left cell facing right.
2. Emit the current cell and mark it visited.
3. Compute the next cell in the current direction; if it is out of bounds or already visited, advance the direction index `(direction_idx + 1) % 4` and recompute.
4. Move to the next cell and repeat for `m × n` total steps.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m×n)`

Each of the `m × n` cells is processed once in the main loop.

##### Space Complexity: `O(m×n)`

A full `visited` matrix is allocated to track which cells have been consumed.

#### Key Insights

- The most self-derivable starting point: simulate the walk and turn whenever you hit a wall or a cell you have already seen.
- Encoding turns as a cyclic index into a direction vector list makes the rotation logic clean and systematic.
- The pattern generalizes well to other path-finding and grid-traversal problems.
- The visited array trades `O(m×n)` extra space for trivially simple turn detection, which later approaches eliminate.

### State Machine

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """
        State machine with explicit state transitions
        """
        if not matrix or not matrix[0]:
            return []

        m, n = len(matrix), len(matrix[0])
        result = []
        visited = [[False] * n for _ in range(m)]

        # States: 0=right, 1=down, 2=left, 3=up
        state = 0
        row, col = 0, 0

        for _ in range(m * n):
            result.append(matrix[row][col])
            visited[row][col] = True

            # Determine next position based on current state
            if state == 0:  # Moving right
                if col + 1 < n and not visited[row][col + 1]:
                    col += 1
                else:
                    state = 1  # Switch to moving down
                    row += 1
            elif state == 1:  # Moving down
                if row + 1 < m and not visited[row + 1][col]:
                    row += 1
                else:
                    state = 2  # Switch to moving left
                    col -= 1
            elif state == 2:  # Moving left
                if col - 1 >= 0 and not visited[row][col - 1]:
                    col -= 1
                else:
                    state = 3  # Switch to moving up
                    row -= 1
            else:  # state == 3, moving up
                if row - 1 >= 0 and not visited[row - 1][col]:
                    row -= 1
                else:
                    state = 0  # Switch to moving right
                    col += 1

        return result
```

#### Approach

This is the same walk-and-turn simulation as the previous solution, with the direction held as an explicit state (`0=right, 1=down, 2=left, 3=up`) and the turn logic spelled out per state instead of through a direction vector list. After emitting and marking the current cell, the active state decides the next move: continue in the current direction while the adjacent cell is in bounds and unvisited, otherwise advance the state to the next direction and step that way instead. Running for `m × n` steps emits all cells in spiral order.

1. Allocate a `visited` grid and start at the top-left cell in state `0` (right).
2. Emit the current cell and mark it visited.
3. Inspect the adjacent cell in the current state's direction; if it is in bounds and unvisited, step there, otherwise advance the state and step in the new direction.
4. Repeat for `m × n` total steps.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m×n)`

The loop runs once per cell, performing constant work each iteration.

##### Space Complexity: `O(m×n)`

A `visited` matrix is maintained to decide when each state transition should fire.

#### Key Insights

- A refinement of the direction-vector walk that unrolls the turn rule into one explicit branch per direction.
- The explicit per-state transition logic makes the approach easy to extend when a problem variation needs custom behavior at each direction.
- It still relies on the same `O(m×n)` visited array, so it does not improve on the brute force's space cost.

### Boundary Simulation

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """
        Traverse matrix using four boundaries that shrink inward
        """
        if not matrix or not matrix[0]:
            return []

        result = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1

        while top <= bottom and left <= right:
            # Traverse right along top row
            for col in range(left, right + 1):
                result.append(matrix[top][col])
            top += 1

            # Traverse down along right column
            for row in range(top, bottom + 1):
                result.append(matrix[row][right])
            right -= 1

            # Traverse left along bottom row (if row still exists)
            if top <= bottom:
                for col in range(right, left - 1, -1):
                    result.append(matrix[bottom][col])
                bottom -= 1

            # Traverse up along left column (if column still exists)
            if left <= right:
                for row in range(bottom, top - 1, -1):
                    result.append(matrix[row][left])
                left += 1

        return result
```

#### Approach

Once you notice the walk only ever needs to know which ring it is on, the `visited` array becomes unnecessary. Maintain four boundaries (`top`, `bottom`, `left`, `right`) that mark the current outer ring, then peel that ring off one edge at a time. Traverse the top row left to right and shrink `top`, the right column top to bottom and shrink `right`, the bottom row right to left and shrink `bottom`, then the left column bottom to top and shrink `left`. The two inner traversals are guarded so a degenerate single remaining row or column is not revisited. The loop repeats until the boundaries cross.

1. Initialize `top`, `bottom`, `left`, `right` to the matrix edges.
2. Emit the top row left to right, then increment `top`.
3. Emit the right column top to bottom, then decrement `right`.
4. If a row remains, emit the bottom row right to left, then decrement `bottom`.
5. If a column remains, emit the left column bottom to top, then increment `left`.
6. Repeat until the boundaries cross.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m×n)`

Every cell of the matrix is appended to the result exactly once.

##### Space Complexity: `O(1)`

Only four integer boundaries are tracked; no auxiliary structure beyond the required output is used.

#### Key Insights

- The refinement that drops the visited array entirely: tracking the four shrinking boundaries is all the state the spiral needs.
- The guards `if top <= bottom` and `if left <= right` cleanly handle single-row and single-column edge cases.
- This is the classic interview answer, achieving `O(1)` auxiliary space without sacrificing clarity.

### Layer-by-Layer Recursive

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """
        Recursive approach - process outer layer then recurse on inner matrix
        """
        def spiral_helper(top, bottom, left, right):
            if top > bottom or left > right:
                return []

            result = []

            # Single row case
            if top == bottom:
                return [matrix[top][col] for col in range(left, right + 1)]

            # Single column case
            if left == right:
                return [matrix[row][left] for row in range(top, bottom + 1)]

            # Traverse the outer layer
            # Right
            for col in range(left, right + 1):
                result.append(matrix[top][col])

            # Down (excluding corners already processed)
            for row in range(top + 1, bottom + 1):
                result.append(matrix[row][right])

            # Left (excluding corners)
            for col in range(right - 1, left - 1, -1):
                result.append(matrix[bottom][col])

            # Up (excluding corners)
            for row in range(bottom - 1, top, -1):
                result.append(matrix[row][left])

            # Recurse on inner matrix
            return result + spiral_helper(top + 1, bottom - 1, left + 1, right - 1)

        if not matrix or not matrix[0]:
            return []

        return spiral_helper(0, len(matrix) - 1, 0, len(matrix[0]) - 1)
```

#### Approach

Treat the matrix as a set of nested rings and process one ring per call. The helper walks the outer layer (top row right, right column down, bottom row left, left column up, skipping already-visited corners), then recurses on the inner rectangle defined by `top + 1, bottom - 1, left + 1, right - 1`. Dedicated base cases handle a single remaining row or column, and an empty range stops the recursion.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m×n)`

Each cell belongs to exactly one ring and is visited a single time across all recursive calls.

##### Space Complexity: `O(min(m,n))`

The recursion depth equals the number of rings, which is bounded by `min(m, n) / 2`.

#### Key Insights

- Elegant divide-and-conquer decomposition: peel the outer ring, then solve the smaller inner matrix.
- Explicit single-row and single-column base cases handle edge cases cleanly.
- The recursive call stack makes execution harder to trace and debug than the iterative variants.

### Transpose and Reverse Pattern

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """
        Pattern-based approach using matrix transformations
        """
        if not matrix or not matrix[0]:
            return []

        result = []

        while matrix:
            # Take the first row
            result.extend(matrix.pop(0))

            if matrix and matrix[0]:
                # Take the last element of each remaining row (right column)
                for row in matrix:
                    result.append(row.pop())

            if matrix:
                # Take the last row in reverse (bottom row, right to left)
                result.extend(matrix.pop()[::-1])

            if matrix and matrix[0]:
                # Take the first element of each remaining row in reverse order (left column, bottom to top)
                for row in reversed(matrix):
                    result.append(row.pop(0))

        return result
```

#### Approach

Repeatedly strip the outer edges off the matrix using list operations. Pop the first row and extend the result with it, then pop the last element of every remaining row to capture the right column, then pop and reverse the last row for the bottom edge, then pop the first element of each remaining row in reverse order for the left column. Each pass consumes one ring, and the loop continues until the matrix is empty.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m×n)`

Every element is popped and appended exactly once over the life of the loop.

##### Space Complexity: `O(1)`

The algorithm uses only `O(1)` auxiliary space, but it achieves that by destructively mutating the input matrix in place rather than preserving the original.

#### Key Insights

- Compact, pattern-based code that showcases Python list manipulation (`pop`, slicing, `reversed`).
- Destructive: it modifies the input matrix, so it cannot be used when the caller must preserve the original.
- The transformation-based flow is less intuitive to read than explicit boundary tracking.

## Comparison of Solutions

### Time Complexity

- **Direction Vector Walk**: `O(m×n)` - one step per cell with constant-time turn checks.
- **State Machine**: `O(m×n)` - one loop iteration per cell.
- **Boundary Simulation**: `O(m×n)` - each cell is appended once as the boundaries shrink.
- **Layer-by-Layer Recursive**: `O(m×n)` - each cell belongs to exactly one ring.
- **Transpose and Reverse**: `O(m×n)` - every element is popped and appended once.

### Space Complexity

- **Direction Vector Walk**: `O(m×n)` - a full visited matrix is allocated.
- **State Machine**: `O(m×n)` - a visited matrix drives the transitions.
- **Boundary Simulation**: `O(1)` - only four integer boundaries are tracked.
- **Layer-by-Layer Recursive**: `O(min(m,n))` - recursion depth equals the number of rings.
- **Transpose and Reverse**: `O(1)` auxiliary, but it mutates the input matrix in place.

### Trade-offs

- **Direction Vector Walk** is the most self-derivable solution, simulating the walk and turning at walls or visited cells, paying for that simplicity with `O(m×n)` visited-array space.
- **State Machine** restates the same walk with explicit per-state transitions, which is easy to extend but more verbose and uses the same visited array.
- **Boundary Simulation** drops the visited array for `O(1)` space by tracking four shrinking boundaries, at the cost of careful single-row/column guard handling.
- **Layer-by-Layer Recursive** offers elegant divide-and-conquer decomposition with clean base cases, but spends `O(min(m,n))` stack space and is harder to trace when debugging.
- **Transpose and Reverse** is creative and compact, but it destructively modifies the input and reads less intuitively.

### When to Use Each

- **Direction Vector Walk**: The intuitive starting point, and natural when the spiral is part of a broader grid/path-finding problem where direction vectors generalize.
- **State Machine**: When the traversal needs custom per-direction behavior or future state-specific extensions.
- **Boundary Simulation**: The recommended default for interviews and production: `O(1)` space, no visited array, and widely expected.
- **Layer-by-Layer Recursive**: When a divide-and-conquer framing or layer-wise reasoning is clearer for the audience.
- **Transpose and Reverse**: When code brevity is prized and mutating the input matrix is acceptable.

### Optimization Notes

- **Direction Vector Walk**: `O(m×n)` time, `O(m×n)` space, does not modify the input; its key advantage is being the most intuitive walk-and-turn simulation.
- **State Machine**: `O(m×n)` time, `O(m×n)` space, does not modify the input; its key advantage is explicit, extensible state management.
- **Boundary Simulation**: `O(m×n)` time, `O(1)` space, does not modify the input; its key advantage is eliminating the visited array entirely.
- **Layer-by-Layer Recursive**: `O(m×n)` time, `O(min(m,n))` space, does not modify the input; its key advantage is an elegant divide-and-conquer decomposition.
- **Transpose and Reverse**: `O(m×n)` time, `O(1)` auxiliary space but it modifies the input matrix in place; its key advantage is creative, compact pattern-based code.
- All five solutions share the same `O(m×n)` time bound; they differ in space usage and constant-factor overhead.
- The ladder runs from the visited-array walk (Direction Vector Walk and State Machine) to boundary tracking (Boundary Simulation), which drops the `O(m×n)` visited array for `O(1)` space.
- Single-row and single-column matrices are the recurring edge case; boundary-based approaches need explicit guards to avoid double-counting them.
- Boundary Simulation is the most commonly expected interview answer and demonstrates clear algorithmic thinking.
- The spiral/layer-wise traversal pattern recurs across many matrix problems, so understanding multiple approaches builds a strong, generalizable foundation.
