# [Course Schedule](https://leetcode.com/problems/course-schedule/)

**Medium** | **30 minutes** | **Depth-First Search, Breadth-First Search, Graph, Topological Sort**

**Pattern:** [Graph Traversal](../patterns/graph/intuition.md), [Topological Sort](../patterns/topological_sort/intuition.md)

**Practice:** [`practice/course_schedule/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/course_schedule/solution.py)

There are a total of `numCourses` courses you have to take, labeled from `0` to
`numCourses - 1`. You are given an array `prerequisites` where
`prerequisites[i] = [ai, bi]` indicates that you must take course `bi` first if
you want to take course `ai`. For example, the pair `[0, 1]` indicates that to
take course `0` you have to first take course `1`.

Return `true` if you can finish all courses. Otherwise, return `false`.

## Examples

### Example 1

**Input:** `numCourses = 2`, `prerequisites = [[1,0]]`

**Output:** `true`

**Explanation:** There are a total of `2` courses to take. To take course `1`
you should have finished course `0`. So it is possible.

### Example 2

**Input:** `numCourses = 2`, `prerequisites = [[1,0],[0,1]]`

**Output:** `false`

**Explanation:** To take course `1` you should have finished course `0`, and to
take course `0` you should also have finished course `1`. So it is impossible.

## Constraints

- `1 <= numCourses <= 2000`
- `0 <= prerequisites.length <= 5000`
- `prerequisites[i].length == 2`
- `0 <= ai, bi < numCourses`
- All the pairs `prerequisites[i]` are unique.

## Solutions

### DFS Three-Color

```python
from typing import List


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        WHITE, GRAY, BLACK = 0, 1, 2

        # graph[prereq] holds every course that directly depends on prereq.
        graph: List[List[int]] = [[] for _ in range(numCourses)]
        for course, prereq in prerequisites:
            graph[prereq].append(course)

        color = [WHITE] * numCourses

        def has_cycle(node: int) -> bool:
            if color[node] == GRAY:  # Back edge into the current path -> cycle.
                return True
            if color[node] == BLACK:  # Already fully explored, no cycle here.
                return False

            color[node] = GRAY
            for neighbor in graph[node]:
                if has_cycle(neighbor):
                    return True
            color[node] = BLACK
            return False

        for node in range(numCourses):
            if color[node] == WHITE and has_cycle(node):
                return False
        return True
```

#### Approach

Model the courses as a directed graph: each course is a vertex, and a
prerequisite pair `[a, b]` becomes an edge from `b` to `a`. Every course can be
finished if and only if this graph has no cycle, because a cycle is a set of
courses that mutually depend on one another.

Detect the cycle with a depth-first search that colors each vertex:

1. Build the adjacency list, pointing each prerequisite at the courses that
   depend on it.
2. Mark every vertex `WHITE` (unvisited).
3. Run DFS from each `WHITE` vertex. On entry, paint the vertex `GRAY` to mark
   it as part of the active recursion path.
4. If DFS reaches a `GRAY` vertex, that is a back edge to an ancestor in the
   current path, which proves a cycle exists, so return `false`.
5. After exploring all of a vertex's neighbors, paint it `BLACK` to record that
   it is fully processed and can never participate in a cycle reached later.

If no DFS ever revisits a `GRAY` vertex, the graph is acyclic and every course
can be finished.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V + E)`

Where `V` is `numCourses` and `E` is the number of prerequisite pairs. Building
the graph touches each edge once, and the three-color DFS visits each vertex and
traverses each edge at most once.

##### Space Complexity: `O(V + E)`

The adjacency list stores all `E` edges, the color array uses `O(V)`, and the
recursion stack reaches depth `O(V)` in the worst case.

#### Key Insights

- A simple binary visited flag is not enough for a directed graph; the distinct
  `GRAY` state is what distinguishes a back edge (cycle) from a cross or forward
  edge into an already finished branch.
- Painting a vertex `BLACK` lets later searches skip work that is known to be
  cycle-free, which keeps the traversal linear.
- The check naturally covers disconnected graphs because the outer loop starts a
  DFS from every still-`WHITE` vertex.

### DFS with Recursion Stack

```python
from typing import List


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # graph[course] holds the prerequisites that course depends on.
        graph: List[List[int]] = [[] for _ in range(numCourses)]
        for course, prereq in prerequisites:
            graph[course].append(prereq)

        visited = set()  # Courses fully proven cycle-free.
        path = set()      # Courses on the active recursion path.

        def has_cycle(course: int) -> bool:
            if course in path:  # Revisiting a course already on the path -> cycle.
                return True
            if course in visited:
                return False

            path.add(course)
            visited.add(course)
            for prereq in graph[course]:
                if has_cycle(prereq):
                    return True
            path.remove(course)  # Backtrack: leave the active path.
            return False

        for course in range(numCourses):
            if course not in visited and has_cycle(course):
                return False
        return True
```

#### Approach

This variant detects the same cycle but tracks state with two explicit sets
rather than a color array, which some find clearer to reason about. It also
orients the graph the other way, from each course to its prerequisites, so the
recursion walks dependencies before the course that needs them.

1. Build the adjacency list mapping each course to the courses it requires.
2. Keep a `visited` set of fully processed courses and a `path` set of courses
   currently on the recursion stack.
3. For each unvisited course, run DFS. Add the course to both sets on entry.
4. If DFS reaches a course already in `path`, the recursion has looped back on
   itself, so a cycle exists and the answer is `false`.
5. After exploring a course's prerequisites, remove it from `path` (backtrack)
   while leaving it in `visited`, so future searches skip it.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V + E)`

Each course and prerequisite edge is processed at most once across the whole
traversal.

##### Space Complexity: `O(V + E)`

The adjacency list holds `O(V + E)`, the `visited` and `path` sets each hold up
to `O(V)` entries, and the recursion stack reaches `O(V)` depth.

#### Key Insights

- The `path` set is the set-based equivalent of the `GRAY` color: membership in
  it means the vertex is an ancestor on the current recursion path.
- Removing a course from `path` on the way out is essential; without the
  backtrack, sibling branches would falsely look like cycles.
- Keeping `visited` separate from `path` avoids re-exploring shared subgraphs,
  preserving the linear time bound.

### Kahn's Algorithm

```python
from collections import deque
from typing import List


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # graph[prereq] holds the courses that depend on prereq.
        graph: List[List[int]] = [[] for _ in range(numCourses)]
        in_degree = [0] * numCourses
        for course, prereq in prerequisites:
            graph[prereq].append(course)
            in_degree[course] += 1

        # Start with every course that has no outstanding prerequisites.
        queue = deque(i for i in range(numCourses) if in_degree[i] == 0)
        completed = 0

        while queue:
            node = queue.popleft()
            completed += 1
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return completed == numCourses
```

#### Approach

Kahn's algorithm performs a topological sort with BFS. The key observation is
that in an acyclic dependency graph there is always at least one course with no
remaining prerequisites, so we can finish courses one in-degree-zero layer at a
time.

1. Build the adjacency list and an in-degree array counting how many
   prerequisites each course still needs.
2. Seed a queue with every course whose in-degree is `0`.
3. Pop a course, count it as completed, and decrement the in-degree of each
   course that depended on it. Whenever a dependent course drops to in-degree
   `0`, enqueue it.
4. Continue until the queue empties.

If every course was completed, a full topological order exists and the graph is
acyclic. If some courses never reached in-degree `0`, they are trapped in a
cycle, so return `false`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V + E)`

Building the graph is `O(E)`, and the BFS dequeues each course once and relaxes
each edge once, for `O(V + E)` overall.

##### Space Complexity: `O(V + E)`

The adjacency list uses `O(V + E)`, while the in-degree array and the queue each
use `O(V)`.

#### Key Insights

- The number of completed courses is the cycle test: any shortfall against
  `numCourses` means at least one course never lost all its prerequisites.
- The algorithm is iterative, so it avoids the deep recursion that DFS can hit on
  long dependency chains near the constraint limit.
- The processing order is itself a valid course schedule, which is useful when
  the problem later asks for the order rather than a yes/no answer.

## Comparison of Solutions

### Time Complexity

- **DFS Three-Color**: `O(V + E)` - visits each vertex and edge at most once.
- **DFS with Recursion Stack**: `O(V + E)` - identical traversal, tracked with
  sets instead of a color array.
- **Kahn's Algorithm**: `O(V + E)` - dequeues each course once and relaxes each
  edge once.

### Space Complexity

- **DFS Three-Color**: `O(V + E)` - adjacency list plus the color array and
  recursion stack.
- **DFS with Recursion Stack**: `O(V + E)` - adjacency list plus the `visited`
  and `path` sets and recursion stack.
- **Kahn's Algorithm**: `O(V + E)` - adjacency list plus the in-degree array and
  BFS queue.

### Trade-offs

- **DFS Three-Color**: Direct and compact cycle detection, but it relies on
  recursion that can be deep on long chains.
- **DFS with Recursion Stack**: Set-based state can read more clearly than color
  codes, at the cost of higher constant factors than an integer array.
- **Kahn's Algorithm**: Iterative and produces a usable topological order, at the
  cost of a slightly more involved in-degree setup.

### When to Use Each

- **DFS Three-Color** (recommended): Best for interviews; it states the core idea
  of finding a back edge in a directed graph as directly as possible.
- **DFS with Recursion Stack**: When explicit `visited`/`path` sets are clearer to
  the reader than a numeric color state.
- **Kahn's Algorithm**: When you also need the concrete ordering or prefer an
  iterative solution that avoids deep recursion on large graphs.

### Optimization Notes

- The three-state coloring is essential: a node found in the `GRAY` state signals
  a cycle, whereas a plain visited flag would miss back edges in a directed
  graph.
- Union-Find is not appropriate here. It detects cycles in undirected graphs and
  cannot distinguish `[a, b]` from `[b, a]`, so it would report false cycles or
  miss real ones for directed prerequisites.
- For graphs near the constraint limit, Kahn's iterative BFS sidesteps the
  recursion-depth risk that the DFS approaches carry on long dependency chains.
