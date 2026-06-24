# [Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/)

**Medium** | **30 minutes** | **Depth-First Search, Breadth-First Search, Graph, Topological Sort**

**Pattern:** [Topological Sort](../patterns/topological_sort/intuition.md)

**Practice:** [`practice/minimum_height_trees/solution.py`](../../practice/minimum_height_trees/solution.py)

A tree is an undirected graph in which any two vertices are connected by exactly one path. In other words, any connected graph without simple cycles is a tree.

Given a tree of n nodes labelled from 0 to n - 1, and an array of n - 1 edges where edges[i] = [ai, bi] indicates that there is an undirected edge between the two nodes ai and bi in the tree, you can choose any node of the tree as the root. When you pick a node x as the root, the resulting tree has height h. Among all possible rooted trees, those with minimum height h are called **minimum height trees** (MHTs).

Return a list of all MHTs' root labels. You can return the answer in **any order**.

The **height** of a rooted tree is the number of edges on the longest downward path between the root and a leaf.

## Examples

### Example 1

![Tree Example 1](assets/minimum_height_trees_example1.jpg)

**Input:** n = 4, edges = `[[1,0],[1,2],[1,3]]`

**Output:** `[1]`

**Explanation:** As shown, the height of the tree is 1 when the root is the node with label 1 which is the only MHT.

### Example 2

![Tree Example 2](assets/minimum_height_trees_example2.jpg)

**Input:** n = 6, edges = `[[3,0],[3,1],[3,2],[3,4],[5,4]]`

**Output:** `[3,4]`

**Explanation:** The tree can be rooted at nodes 3 or 4 to achieve minimum height of 2.

## Constraints

- `1 <= n <= 2 * 10^4`
- `edges.length == n - 1`
- `0 <= ai, bi < n`
- `ai != bi`
- All the pairs `(ai, bi)` are distinct.
- The given input is **guaranteed** to be a tree and there will be **no repeated** edges.

## Solutions

### Brute Force BFS From Every Root

```python
from collections import defaultdict, deque


class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        # A single node has height 0 and is the only possible root.
        if n == 1:
            return [0]

        # Build an undirected adjacency list.
        adj = defaultdict(list)
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        def height_from(root: int) -> int:
            # BFS layer by layer; the depth of the last layer is the height.
            seen = {root}
            queue = deque([root])
            depth = -1
            while queue:
                depth += 1
                for _ in range(len(queue)):
                    node = queue.popleft()
                    for nxt in adj[node]:
                        if nxt not in seen:
                            seen.add(nxt)
                            queue.append(nxt)
            return depth

        heights = [height_from(root) for root in range(n)]
        best = min(heights)
        return [root for root in range(n) if heights[root] == best]
```

#### Approach

The problem asks directly for the roots that minimize tree height, so the most
literal solution is to compute that height for every candidate root and keep the
minimizers.

1. Handle `n == 1` up front: a lone node has height 0 and is the only root.
2. Build an undirected adjacency list from the edge list.
3. For each node, run a breadth-first search from that node and record how many
   layers it takes to reach the farthest node. That layer count is the height of
   the tree rooted there.
4. Find the minimum height across all roots and return every root that achieves
   it.

This is the definition translated straight into code. It is easy to reason about
and trivially correct, but it pays for that simplicity by re-traversing the whole
tree once per node.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each BFS visits all `n` nodes and `n - 1` edges, costing `O(n)`. Running one BFS
per root multiplies that by `n`, giving `O(n^2)`. For `n` up to `2 * 10^4` this
is on the order of `4 * 10^8` operations, which is too slow for the largest
inputs but fine for understanding the problem.

##### Space Complexity: `O(n)`

The adjacency list stores `2(n - 1)` endpoints, and each BFS uses a `seen` set and
a queue holding at most `O(n)` nodes. The `heights` array adds another `O(n)`.

#### Key Insights

- The height of a rooted tree equals the number of BFS layers minus one, so a
  single level-order traversal yields it without any extra bookkeeping.
- Multiple roots can tie for the minimum height, so the answer is collected as
  every root matching `best`, not just the first one found.
- This approach never exploits the structure of a tree beyond connectivity, which
  is exactly why it is quadratic and motivates the leaf-trimming refinement.

#### Walkthrough

Let us trace the brute force solution on Example 1: `n = 4` and
`edges = [[1,0],[1,2],[1,3]]`. The expected output is `[1]`.

First we skip the `n == 1` guard (here `n` is 4) and build the adjacency list by
adding both directions of every edge:

- `[1,0]`: `adj[1] = [0]`, `adj[0] = [1]`
- `[1,2]`: `adj[1] = [0, 2]`, `adj[2] = [1]`
- `[1,3]`: `adj[1] = [0, 2, 3]`, `adj[3] = [1]`

So node `1` is the center connected to the three leaves `0`, `2`, and `3`. Now we
call `height_from(root)` once per root. Each call runs a BFS layer by layer and
returns `depth`, the number of layers minus one.

Tracing `height_from(0)`: `seen = {0}`, `queue = [0]`, `depth = -1`.

| Layer | `depth` | nodes popped this layer | neighbors enqueued | `queue` after |
| --- | --- | --- | --- | --- |
| 1 | `0` | `0` | `1` | `[1]` |
| 2 | `1` | `1` | `2`, `3` (0 already seen) | `[2, 3]` |
| 3 | `2` | `2`, `3` | none | `[]` |

The queue empties, so `height_from(0)` returns `depth = 2`. Rooting at a leaf, the
farthest node is two edges away.

Tracing `height_from(1)`: `seen = {1}`, `queue = [1]`, `depth = -1`.

| Layer | `depth` | nodes popped this layer | neighbors enqueued | `queue` after |
| --- | --- | --- | --- | --- |
| 1 | `0` | `1` | `0`, `2`, `3` | `[0, 2, 3]` |
| 2 | `1` | `0`, `2`, `3` | none | `[]` |

`height_from(1)` returns `depth = 1`. Rooting at the center, every leaf is just one
edge away. By symmetry `height_from(2)` and `height_from(3)` each behave like
`height_from(0)` and return `2`.

Collecting the results gives `heights = [2, 1, 2, 2]`. Then `best = min(heights) = 1`,
and we keep every root whose height equals `best`. Only index `1` qualifies, so we
return `[1]`, which matches the expected Output.

### Leaf-Trimming BFS

```python
from collections import deque


class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        # A single node (and trivially two nodes) is its own centroid.
        if n <= 2:
            return list(range(n))

        # Build the adjacency list and track each node's degree.
        adj = [set() for _ in range(n)]
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)

        # Start from all current leaves (degree-1 nodes).
        leaves = deque(node for node in range(n) if len(adj[node]) == 1)

        # Peel leaves layer by layer until 1 or 2 centroids remain.
        remaining = n
        while remaining > 2:
            layer_size = len(leaves)
            remaining -= layer_size
            for _ in range(layer_size):
                leaf = leaves.popleft()
                # Detach this leaf; its single neighbor may become a new leaf.
                neighbor = adj[leaf].pop()
                adj[neighbor].remove(leaf)
                if len(adj[neighbor]) == 1:
                    leaves.append(neighbor)

        # Whatever survives are the roots of the minimum height trees.
        return list(leaves)
```

#### Approach

The roots that minimize tree height are the *centroids* of the tree, the nodes
that sit in the middle of its longest path. A tree always has exactly one or two
centroids, and a brute-force "try every root and BFS" approach would cost
`O(n^2)`. Instead we find the centroids directly by repeatedly trimming the
outermost layer of leaves, which is topological sorting specialized to an
undirected tree.

1. Handle the tiny cases: if `n <= 2`, every node is a valid root, so return all
   of them.
2. Build an adjacency set for each node so leaf removal is `O(1)`.
3. Collect all current leaves (nodes of degree 1) into a queue.
4. Peel one full layer of leaves at a time. Removing a leaf decrements its
   neighbor's degree; a neighbor that drops to degree 1 becomes a leaf in the
   next layer.
5. Stop when 2 or fewer nodes remain. Those survivors are the centroids and thus
   the MHT roots.

Trimming layer by layer shrinks the tree symmetrically from both ends of its
longest path. The last nodes standing are the midpoints of that path, which is
precisely where a root minimizes the maximum distance to any leaf.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Building the adjacency structure visits each of the `n - 1` edges once. During
trimming, every node is enqueued and removed at most once, and each edge is
detached once, so the peeling phase is also linear. The total is `O(n)`.

##### Space Complexity: `O(n)`

The adjacency sets store `2(n - 1)` endpoint entries (`O(n)`), and the leaf queue
holds at most `O(n)` nodes at once.

#### Key Insights

- A tree has at most two centroids, which is why trimming halts at 1 or 2 nodes
  and why the answer never has more than two roots.
- Peeling leaves layer by layer is equivalent to advancing inward from both ends
  of the tree's longest path simultaneously; the centroids are its midpoints.
- Tracking a per-layer `layer_size` (instead of just emptying the queue) ensures
  we remove exactly one ring of leaves per round, which keeps the symmetric
  shrinking correct.
- The `n <= 2` guard is essential: with one or two nodes there are no degree-1
  leaves to peel in the usual sense, so the loop would never start.
- Using adjacency *sets* rather than lists makes detaching a leaf from its
  neighbor an O(1) operation instead of a linear scan.

## Comparison of Solutions

### Time Complexity

- **Brute Force BFS From Every Root**: `O(n^2)` - one BFS per node, each linear in
  the tree size.
- **Leaf-Trimming BFS**: `O(n)` - every node is enqueued once and every edge is
  detached once across the whole peeling process.

### Space Complexity

- **Brute Force BFS From Every Root**: `O(n)` - adjacency list plus the per-BFS
  `seen` set, queue, and the `heights` array.
- **Leaf-Trimming BFS**: `O(n)` - adjacency sets plus a leaf queue.

### Trade-offs

- The brute force version maps the problem statement directly onto code, so it is
  easy to write and verify, but it discards the tree structure and re-traverses
  the entire graph from every node.
- The leaf-trimming version trades a small conceptual leap (the answer is the one
  or two centroids of the tree) for a linear runtime, making it the only viable
  choice near the upper constraint of `n = 2 * 10^4`.

### When to Use Each

- **Brute Force BFS From Every Root**: A small `n`, an interview warm-up, or a
  reference implementation to validate the optimized solution against.
- **Leaf-Trimming BFS** (recommended): Any input that can approach the constraint
  ceiling, where the quadratic approach would time out.

### Optimization Notes

- Both solutions can share the same adjacency build; the leaf-trimming variant
  additionally needs degree information, which adjacency sets provide for free via
  `len(adj[node])`.
- The leaf-trimming loop stops at `remaining <= 2` rather than emptying the queue,
  which is what guarantees the survivors are the centroids instead of an empty
  set.
- For correctness checks, the brute force result can be compared against the
  leaf-trimming result on random trees; they must agree on every input.
