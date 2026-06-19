# [Number of Islands](https://leetcode.com/problems/number-of-islands/)

**Medium** | **25 minutes** | **Array, DFS, BFS, Union Find, Matrix**

**Pattern:** [Graph Traversal](../patterns/graph/intuition.md)

**Practice:** [`practice/number_of_islands/solution.py`](../../practice/number_of_islands/solution.py)

Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands.

An **island** is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.

## Examples

### Example 1

**Input:**

```
grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
```

**Output:** `1`

### Example 2

**Input:**

```
grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
```

**Output:** `3`

## Constraints

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 300`
- `grid[i][j]` is `'0'` or `'1'`.

## Solutions

### DFS with Grid Modification

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        islands = 0

        def dfs(row, col):
            # Base cases: out of bounds or already visited/water
            if (row < 0 or row >= rows or
                col < 0 or col >= cols or
                grid[row][col] == '0'):
                return

            # Mark current cell as visited by changing it to '0'
            grid[row][col] = '0'

            # Recursively explore all 4 adjacent directions
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
            for dr, dc in directions:
                dfs(row + dr, col + dc)

        # Iterate through every cell in the grid
        for row in range(rows):
            for col in range(cols):
                # If we find an unvisited land cell, it's a new island
                if grid[row][col] == '1':
                    islands += 1
                    # Use DFS to mark all connected land cells as visited
                    dfs(row, col)

        return islands
```

#### Approach

This DFS solution treats each unvisited land cell ('1') as the start of a new island. When we encounter such a cell, we increment our island count and use DFS to explore and mark all connected land cells as visited (by changing them to '0').

The key insight is that we're finding connected components in an implicit graph where:
- Each land cell is a node
- Adjacent land cells are connected by edges
- Each connected component represents one island

DFS naturally explores the entire connected component before returning, ensuring we count each island exactly once.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

In the worst case (all land), we visit each cell exactly once: once in the main loop and potentially once during DFS traversal.

##### Space Complexity: `O(m × n)`

In the worst case (single snake-like island), the recursion stack can be as deep as the total number of cells. The algorithm modifies the input grid in-place.

#### Key Insights

- Each unvisited `'1'` is the seed of exactly one island; the flood fill guarantees the rest of that island is sunk before the main loop advances.
- Sinking visited land to `'0'` doubles as the visited marker, so no extra bookkeeping structure is needed.
- The four-direction flood fill matches the adjacency rule (horizontal and vertical only), so diagonally touching cells stay separate islands.

### BFS with Grid Modification

```python
from collections import deque

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        islands = 0

        def bfs(start_row, start_col):
            queue = deque([(start_row, start_col)])
            grid[start_row][start_col] = '0'  # Mark as visited immediately

            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

            while queue:
                row, col = queue.popleft()

                # Check all 4 adjacent directions
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc

                    # If adjacent cell is valid land, add to queue and mark as visited
                    if (0 <= new_row < rows and
                        0 <= new_col < cols and
                        grid[new_row][new_col] == '1'):

                        grid[new_row][new_col] = '0'  # Mark as visited
                        queue.append((new_row, new_col))

        # Iterate through every cell in the grid
        for row in range(rows):
            for col in range(cols):
                # If we find an unvisited land cell, it's a new island
                if grid[row][col] == '1':
                    islands += 1
                    # Use BFS to mark all connected land cells as visited
                    bfs(row, col)

        return islands
```

#### Approach

This BFS solution follows the same logic as the DFS approach but uses a queue to explore connected components level by level. BFS can be preferable when dealing with very deep recursion scenarios or when you need to find the shortest path within connected components.

BFS explores nodes in order of their distance from the starting point, which can be useful for certain extensions of this problem.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

Same as DFS: each cell is visited at most once during the entire algorithm.

##### Space Complexity: `O(min(m, n))`

In the worst case (rectangle-shaped island), the BFS queue contains at most `O(min(m, n))` cells, which occurs when the wavefront forms a diagonal. This can be more space-efficient than DFS for certain grid shapes.

#### Key Insights

- Marking a cell visited at enqueue time (rather than dequeue time) prevents the same cell from being added to the queue twice.
- BFS bounds peak memory by the frontier size rather than the longest path, so it sidesteps the deep recursion that can crash DFS on huge grids.
- The traversal order does not affect the island count, so BFS and DFS are interchangeable for correctness here.

### DFS with Separate Visited Array

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        visited = [[False] * cols for _ in range(rows)]
        islands = 0

        def dfs(row, col):
            # Base cases: out of bounds, already visited, or water
            if (row < 0 or row >= rows or
                col < 0 or col >= cols or
                visited[row][col] or
                grid[row][col] == '0'):
                return

            # Mark current cell as visited
            visited[row][col] = True

            # Recursively explore all 4 adjacent directions
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dr, dc in directions:
                dfs(row + dr, col + dc)

        # Iterate through every cell in the grid
        for row in range(rows):
            for col in range(cols):
                # If we find an unvisited land cell, it's a new island
                if grid[row][col] == '1' and not visited[row][col]:
                    islands += 1
                    # Use DFS to mark all connected land cells as visited
                    dfs(row, col)

        return islands
```

#### Approach

This approach preserves the original grid by using a separate visited matrix. This is useful when you need to maintain the original input or when the grid is read-only.

The algorithm is identical to DFS with Grid Modification except we track visited cells in a separate 2D boolean array instead of modifying the input grid.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

Same traversal pattern as previous solutions.

##### Space Complexity: `O(m × n)`

Requires additional space for the visited matrix plus recursion stack space.

#### Key Insights

- Decoupling the visited state from the grid keeps the caller's input intact, which matters when the grid is read-only or reused afterward.
- The cost is an explicit `O(m × n)` boolean matrix, the price of not mutating the input.
- The visited check must come before the water check in the guard to short-circuit revisits cleanly.

### Iterative DFS with Stack

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        islands = 0

        def iterative_dfs(start_row, start_col):
            stack = [(start_row, start_col)]
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

            while stack:
                row, col = stack.pop()

                # Skip if out of bounds or water/visited
                if (row < 0 or row >= rows or
                    col < 0 or col >= cols or
                    grid[row][col] == '0'):
                    continue

                # Mark as visited
                grid[row][col] = '0'

                # Add all valid neighbors to stack
                for dr, dc in directions:
                    stack.append((row + dr, col + dc))

        # Iterate through every cell in the grid
        for row in range(rows):
            for col in range(cols):
                # If we find an unvisited land cell, it's a new island
                if grid[row][col] == '1':
                    islands += 1
                    # Use iterative DFS to mark all connected land cells
                    iterative_dfs(row, col)

        return islands
```

#### Approach

This solution uses an explicit stack to simulate DFS without recursion, avoiding potential stack overflow issues for very large grids. The logic is identical to recursive DFS but uses a stack data structure instead of the call stack.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

Each cell is processed at most once.

##### Space Complexity: `O(m × n)`

In the worst case, the explicit stack might contain all cells (for a snake-like island).

#### Key Insights

- The explicit stack replaces Python's call stack, so the traversal cannot hit the interpreter recursion limit on a 300 × 300 grid.
- Pushing neighbors first and validating them on pop keeps the inner loop simple, at the cost of occasionally stacking already-sunk cells that are then skipped.
- A cell can appear multiple times on the stack, so the bounds-and-water guard on pop is what guarantees each cell is sunk exactly once.

### Union-Find

```python
class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size
        self.components = size

    def find(self, x):
        # Path compression optimization
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)

        if root_x != root_y:
            # Union by rank optimization
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1

            self.components -= 1

    def get_components(self):
        return self.components

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])

        # Count water cells to subtract from total components later
        water_cells = 0

        # Create Union-Find structure for all cells
        uf = UnionFind(rows * cols)

        def get_index(row, col):
            """Convert 2D coordinates to 1D index"""
            return row * cols + col

        # Process each cell and union with adjacent land cells
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == '0':
                    water_cells += 1
                else:  # Land cell
                    # Check right and down neighbors only (to avoid double processing)
                    directions = [(0, 1), (1, 0)]  # right, down
                    current_idx = get_index(row, col)

                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc

                        # If neighbor is valid land, union them
                        if (0 <= new_row < rows and
                            0 <= new_col < cols and
                            grid[new_row][new_col] == '1'):

                            neighbor_idx = get_index(new_row, new_col)
                            uf.union(current_idx, neighbor_idx)

        # Total islands = total components - water cells
        return uf.get_components() - water_cells
```

#### Approach

Union-Find treats this as a dynamic connectivity problem. We initially consider each cell as a separate component, then union adjacent land cells. The final number of islands equals the number of connected components minus the water cells.

This approach is particularly powerful for scenarios where the grid is built dynamically or when you need to support queries about connectivity between arbitrary cells.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n × α(m × n))`

Where α is the inverse Ackermann function (practically constant). Each cell is processed once, and each union/find operation takes nearly constant time with path compression and union by rank.

##### Space Complexity: `O(m × n)`

Space for the parent and rank arrays in the Union-Find structure.

#### Key Insights

- Unioning only the right and down neighbors covers every adjacency exactly once, avoiding redundant union calls.
- Subtracting the water-cell count from the total component count yields the island count without ever sinking land, so the input grid is preserved.
- Path compression plus union by rank keep each operation effectively constant, which is what makes the structure competitive with linear traversal.

## Comparison of Solutions

### Time Complexity

- **DFS with Grid Modification**: `O(m × n)` - Each cell is visited at most once across the main loop and DFS traversal.
- **BFS with Grid Modification**: `O(m × n)` - Same as DFS, each cell is processed at most once.
- **DFS with Separate Visited Array**: `O(m × n)` - Identical traversal pattern, each cell visited once.
- **Iterative DFS with Stack**: `O(m × n)` - Each cell is processed at most once.
- **Union-Find**: `O(m × n × α(m × n))` - Each cell is processed once, with each union/find operation taking nearly constant inverse-Ackermann time.

### Space Complexity

- **DFS with Grid Modification**: `O(m × n)` - Recursion stack can grow as deep as the cell count for a snake-like island.
- **BFS with Grid Modification**: `O(min(m, n))` - The BFS queue holds at most a diagonal wavefront, which is more space-efficient for wide grids.
- **DFS with Separate Visited Array**: `O(m × n)` - Requires the visited matrix plus recursion stack space.
- **Iterative DFS with Stack**: `O(m × n)` - The explicit stack may contain all cells for a snake-like island.
- **Union-Find**: `O(m × n)` - Parent and rank arrays for every cell.

### Trade-offs

- **DFS with Grid Modification**: Simple, space-efficient, and optimal, but it modifies the input grid.
- **BFS with Grid Modification**: Offers better space usage on wide grids, at the cost of a more complex implementation.
- **DFS with Separate Visited Array**: Preserves the input grid, but requires extra space for the visited matrix.
- **Iterative DFS with Stack**: Avoids recursion depth limits, but requires explicit stack management.
- **Union-Find**: Handles dynamic connectivity scenarios well, but the implementation is complex.

### When to Use Each

- **DFS with Grid Modification (Recommended)**: Best for interviews: simple, optimal, and demonstrates core graph traversal concepts.
- **BFS**: When you need level-order exploration or have memory constraints with deep grids.
- **DFS with Separate Visited**: When input grid must be preserved or is read-only.
- **Iterative DFS**: When dealing with very large grids where recursion depth might be an issue.
- **Union-Find**: For advanced scenarios with dynamic grid updates or connectivity queries.

### Optimization Notes

- DFS with Grid Modification is the recommended interview choice: it is optimal in time, simple to implement, and demonstrates core graph traversal cleanly.
- When the input grid must remain intact, switch to the DFS with Separate Visited Array approach's separate visited array; the only cost is the extra `O(m × n)` matrix.
- For very large grids, prefer BFS or Iterative DFS with Stack to avoid Python's recursion depth limit causing a stack overflow.
- A common pitfall is missing bounds checks before indexing neighbors; the direction array `[(0,1),(1,0),(0,-1),(-1,0)]` with explicit `0 <= r < rows` guards keeps the traversal safe.
