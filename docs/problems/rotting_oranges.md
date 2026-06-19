# [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/)

**Medium** | **30 minutes** | **Array, BFS, Matrix**

**Pattern:** [Multi-Source BFS](../patterns/grid_bfs_multi_source/intuition.md)

**Practice:** [`practice/rotting_oranges/solution.py`](../../practice/rotting_oranges/solution.py)

You are given an `m x n` grid where each cell can have one of three values:

- `0` representing an empty cell,
- `1` representing a fresh orange, or
- `2` representing a rotten orange.

Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return `-1`.

## Examples

### Example 1

![Rotting Oranges Example 1](assets/rotting_oranges_example1.png)

**Input:** `grid = [[2,1,1],[1,1,0],[0,1,1]]`

**Output:** `4`

### Example 2

**Input:** `grid = [[2,1,1],[0,1,1],[1,0,1]]`

**Output:** `-1`

**Explanation:** The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.

### Example 3

**Input:** `grid = [[0,2]]`

**Output:** `0`

**Explanation:** Since there are already no fresh oranges at minute 0, the answer is just 0.

## Constraints

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 10`
- `grid[i][j]` is `0`, `1`, or `2`.

## Solutions

### Simulation

```python
from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        fresh = sum(
            1 for r in range(rows) for c in range(cols) if grid[r][c] == 1
        )

        # No fresh oranges to begin with means zero minutes elapse.
        if fresh == 0:
            return 0

        minutes = 0
        while True:
            # Find every fresh orange that touches a rotten one this minute.
            to_rot = []
            for r in range(rows):
                for c in range(cols):
                    if grid[r][c] == 1:
                        for dr, dc in directions:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 2:
                                to_rot.append((r, c))
                                break

            # No orange rots this minute means we have stalled.
            if not to_rot:
                break

            # Rot them all at once so this minute's spread does not cascade.
            for r, c in to_rot:
                grid[r][c] = 2
                fresh -= 1
            minutes += 1

        # Any fresh orange left unreachable means it can never rot.
        return minutes if fresh == 0 else -1
```

#### Approach

The problem is a literal simulation: each minute, every fresh orange adjacent to
a rotten one becomes rotten, and we count how many minutes pass before the grid
stops changing. The most direct way to model this is to do exactly that, scanning
the whole grid once per minute.

1. Count the fresh oranges. If there are none, return `0` immediately because no
   time has to elapse.
2. Each minute, scan every cell. For each fresh orange, check its four neighbors;
   if any neighbor is rotten, mark this orange for rotting. Collect these into a
   `to_rot` list rather than rotting in place.
3. Deferring the rot is essential. If a fresh orange were marked rotten the
   instant it is found, a later cell in the same scan could see it and rot in the
   same minute, collapsing two minutes of spread into one. Batching the changes
   keeps each minute's spread to a single ring.
4. If a full scan finds no orange to rot, the process has stalled. Stop and
   return `minutes` if no fresh oranges remain, otherwise `-1` for the unreachable
   survivors.

#### Time and Space Complexity Analysis

##### Time Complexity: `O((m × n)²)`

In the worst case the rot advances one ring per minute, which can take up to
`O(m × n)` minutes, and each minute rescans all `m × n` cells. The product gives
a quadratic bound in the number of cells.

##### Space Complexity: `O(m × n)`

The `to_rot` list can hold up to `O(m × n)` positions in a single minute. The
grid is mutated in place, so no separate visited structure is needed.

#### Key Insights

- Direct simulation mirrors the problem statement, which makes it the easiest
  approach to derive and to convince yourself is correct.
- Batching the rotting into `to_rot` and applying it after the scan is the one
  subtlety: rotting in place would let one minute's spread leak into the next.
- The repeated full-grid rescans are wasted work, since most cells do not change
  between minutes. That inefficiency is exactly what the BFS approach removes.

### Multi-Source BFS

```python
from collections import deque
from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])

        # Seed the queue with every rotten orange and count fresh ones.
        queue = deque()
        fresh = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1

        # No fresh oranges to begin with means zero minutes elapse.
        if fresh == 0:
            return 0

        minutes = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # Process the grid one minute (one BFS level) at a time.
        while queue and fresh > 0:
            minutes += 1
            for _ in range(len(queue)):
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2  # rot it now so it isn't queued twice
                        fresh -= 1
                        queue.append((nr, nc))

        # Any fresh orange left unreachable means it can never rot.
        return minutes if fresh == 0 else -1
```

#### Approach

The rot spreads outward from every rotten orange simultaneously, one ring of
neighbors per minute. That "all sources advance together, one step at a time"
behavior is exactly multi-source breadth-first search: seed the BFS frontier
with *all* rotten oranges at once, then expand level by level, where each level
corresponds to one elapsed minute.

1. Scan the grid once. Push every rotten orange (`2`) onto the queue and count
   the fresh oranges (`1`).
2. If there are no fresh oranges, the answer is `0` immediately (nothing has to
   rot, even if the grid is empty of oranges entirely).
3. Run BFS in level order. Before processing each level, increment `minutes`,
   then drain exactly the oranges that were rotten at the start of that minute.
4. For each rotten orange, rot any fresh 4-directional neighbor, decrement the
   fresh count, and enqueue it. Marking it rotten on enqueue prevents the same
   orange from being processed twice.
5. When the queue empties, return `minutes` if no fresh oranges remain,
   otherwise return `-1` because the survivors are unreachable.

Processing a full level per minute is what makes the minute count correct: every
orange enqueued during minute `k` rots its neighbors at minute `k + 1`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

The initial scan touches every cell once. During BFS each cell is enqueued at
most once and dequeued at most once, and each dequeue inspects four neighbors.
Total work is linear in the number of cells.

##### Space Complexity: `O(m × n)`

In the worst case (the whole grid starts rotten) the queue holds every cell at
once. No separate visited structure is needed because the grid itself records
state by flipping `1` to `2`.

#### Key Insights

- Multi-source BFS handles simultaneous spread cleanly: seed every source first,
  then a single level of expansion equals a single minute.
- Counting fresh oranges up front gives an O(1) termination check and lets us
  distinguish "all rotted" from "some unreachable" without re-scanning.
- Rotting a neighbor at enqueue time (not dequeue time) is the standard guard
  that keeps each cell out of the queue more than once.
- The `if fresh == 0: return 0` guard covers the subtle edge case where the grid
  has no fresh oranges, so zero minutes elapse even if rotten oranges exist.
- Looping `for _ in range(len(queue))` snapshots the current frontier size,
  which is the trick that separates one minute's oranges from the next.

## Comparison of Solutions

### Time Complexity

- **Simulation**: `O((m × n)²)` - up to `O(m × n)` minutes, each rescanning all
  `m × n` cells.
- **Multi-Source BFS**: `O(m × n)` - every cell is enqueued and dequeued at most
  once.

### Space Complexity

- **Simulation**: `O(m × n)` - the `to_rot` batch can hold every cell in one
  minute.
- **Multi-Source BFS**: `O(m × n)` - the queue can hold every cell when the whole
  grid starts rotten.

### Trade-offs

- Simulation reads exactly like the problem statement, so it is the quickest to
  write and verify, but it pays for that clarity with repeated full-grid scans.
- Multi-Source BFS touches each cell a constant number of times by tracking the
  active frontier, at the cost of recognizing the spread as a level-order graph
  traversal.

### When to Use Each

- **Simulation**: Reach for it when the grid is small (here `m, n <= 10`) and
  readability matters more than asymptotic speed, or as a correctness reference.
- **Multi-Source BFS** (recommended): The right call for larger grids or when
  optimal linear time is required.

### Optimization Notes

- Both approaches mutate the grid in place to record rotten cells, avoiding a
  separate visited matrix.
- Counting fresh oranges up front gives both an O(1) termination test and a clean
  way to distinguish "all rotted" from "some unreachable."
- The BFS guard of rotting a neighbor at enqueue time (rather than dequeue time)
  is what keeps each cell out of the queue more than once; the simulation's
  equivalent guard is batching changes into `to_rot` before applying them.
