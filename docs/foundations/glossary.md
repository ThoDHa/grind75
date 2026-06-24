# Glossary

Plain-language definitions of the terms that recur across the problem pages and
pattern guides. Each entry links to the foundation or pattern guide where the
idea is developed in full.

**Adjacency list**: the usual way to store a [graph](data_structures.md): a map
from each node to the list of its neighbors. Compact when most nodes have few
connections.

**Amortized**: an average cost per operation taken over many operations. A
single operation may occasionally be slow, but spread across a long run the
average stays low. Hash-map operations are "`O(1)` amortized".

**Backtracking**: building a solution one choice at a time, and undoing the
last choice when it leads nowhere, to try the next option. Developed in the
[Backtracking guide](../patterns/backtracking_exploration/intuition.md).

**Base case**: the smallest input in a [recursion](recursion.md), where the
answer is returned directly with no further recursive calls. It is what stops
the recursion.

**Big-O**: notation describing how work grows with input size. See the
[Big-O guide](big_o.md).

**Bottom-up**: a [dynamic programming](../patterns/dp_1d_linear/intuition.md) style that
starts from the smallest subproblems and builds up to the answer with a loop,
filling a table. Contrast with top-down.

**Breadth-first search (BFS)**: exploring a graph or tree level by level,
nearest nodes first, using a [queue](data_structures.md). Finds shortest paths
in unweighted graphs.

**Call stack**: the computer's record of paused function calls, used to return
to the right place after each call finishes. Central to how
[recursion](recursion.md) works.

**Complement**: the value you still need. In [Two Sum](../problems/two_sum.md),
for a target `t` and current value `x`, the complement is `t - x`, the partner
that completes the pair.

**Depth-first search (DFS)**: exploring a graph or tree by going as deep as
possible down one path before backtracking. Naturally expressed with
[recursion](recursion.md).

**Dynamic programming (DP)**: solving a problem by combining the answers to
overlapping subproblems, each computed once and reused. See the
[DP guide](../patterns/dp_1d_linear/intuition.md).

**In-degree**: the number of edges pointing *into* a node in a directed graph.
Counting in-degrees is the heart of [topological sort](../patterns/topological_sort/intuition.md) by
Kahn's algorithm.

**In-place**: an algorithm that transforms its input using only a constant
amount of extra memory, rather than building a separate copy. Uses `O(1)` extra
space.

**Invariant**: a condition that stays true throughout a loop or algorithm. The
discipline of binary search is keeping the invariant "the answer is still inside
the current range".

**Memoization**: caching the result of a subproblem the first time it is
computed, so later calls with the same input return instantly instead of
recomputing. The bridge from plain [recursion](recursion.md) to
[dynamic programming](../patterns/dp_1d_linear/intuition.md).

**Monotonic**: consistently moving in one direction, only increasing or only
decreasing. Binary search needs a monotonic property; a monotonic stack keeps
its contents in sorted order.

**Overlapping subproblems**: when the same smaller problem is solved many times
across a recursion. Their presence is the signal to apply
memoization or [dynamic programming](../patterns/dp_1d_linear/intuition.md).

**Sentinel**: a dummy node or boundary value added to remove special cases.
[LRU Cache](../problems/lru_cache.md) uses sentinel head and tail nodes so that
inserting and removing never has to check for the empty-list edge case.

**Sliding window**: a moving range over a sequence whose two ends advance to
keep a condition satisfied. See the
[Sliding Window guide](../patterns/sliding_window/intuition.md).

**Time-space trade**: spending extra memory to save time, or vice versa. The
defining move of the [Hashing pattern](../patterns/hashing/intuition.md):
`O(n)` memory buys `O(1)` lookups.

**Top-down**: a [dynamic programming](../patterns/dp_1d_linear/intuition.md) style that starts
from the full problem and recurses into subproblems, using
memoization to avoid repeats. Contrast with bottom-up.

**Topological sort**: an ordering of the nodes of a directed acyclic graph such
that every edge points forward, so all prerequisites come before what depends
on them. See the
[Topological Sort guide](../patterns/topological_sort/intuition.md).

**Two pointers**: two indices moving over a sequence in a coordinated way to
shrink the search space. See the
[Two Pointers guide](../patterns/two_pointers/intuition.md).
