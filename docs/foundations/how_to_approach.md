# How to Approach a Problem

The hardest moment is the blank page: you have read the problem and have no idea
where to start. This guide replaces that panic with a repeatable method. None of
these steps require cleverness. They are a checklist you run every time, and the
clever idea usually appears somewhere in the middle of running it.

## The method

### 1. Understand the problem exactly

Restate it in your own words. Identify the input (its type and size from the
**Constraints**), the output, and any rules. Vague understanding is the most
common cause of wrong solutions, so do not skip this.

### 2. Walk through the examples by hand

Take the provided examples and solve them yourself on paper, slowly. Notice
*how* you arrived at the answer. Your own manual process is very often the
algorithm in disguise. If the examples do not cover an edge case (empty input,
a single element, all-equal values), invent one and solve it too.

### 3. Write the brute force first

Find the most obvious, direct solution, even if it is slow. Try every pair, try
every path, simulate the process literally. This matters for three reasons: it
proves you understand the problem, it gives you a correct answer to check faster
solutions against, and it often reveals the wasted work that the fast solution
will eliminate. On every problem page in this guide, the **Brute Force** is
deliberately the first solution for exactly this reason.

### 4. Find the wasted work

Look at the brute force and ask: what is it recomputing? What does it look at
more than once? The optimization is almost always "remember something so you
do not redo it". A repeated search becomes a hash-map lookup. A recomputed
subproblem becomes a memoized value. A repeated range-sum becomes a prefix sum.

### 5. Recognize the pattern

Most interview problems are one of a small number of patterns wearing a
costume. The signals below point you to the right
[pattern guide](../patterns/index.md), where the mental model is fully
developed.

### 6. Check complexity against the constraints

Before coding, confirm your planned approach is fast enough. Look at the size of
`n` in the **Constraints** and compare it to your approach's
[Big-O](big_o.md). If `n` is 100,000 and your idea is `O(n²)`, stop and find a
better one now, not after writing it.

### 7. Code it, then test the edges

Write the solution, then run it against the examples and the edge cases from
step 2. The places solutions break are almost always the boundaries: empty
input, one element, the first or last position, duplicates, and the largest
allowed value.

## Pattern recognition signals

When you see these clues in a problem, think of the matching pattern:

| Clue in the problem | Likely pattern |
|---------------------|----------------|
| "Have I seen this?", pairs that sum to a target, counting occurrences | [Hashing](../patterns/hashing/intuition.md) |
| Sorted input, "find the position", repeatedly halving | [Binary Search](../patterns/binary_search/intuition.md) |
| Longest or shortest contiguous run that satisfies a condition | [Sliding Window](../patterns/sliding_window/intuition.md) |
| Sorted array, pair or triplet from both ends | [Two Pointers](../patterns/two_pointers/intuition.md) |
| Many range-sum or "product of all except self" queries | [Prefix Sum](../patterns/prefix_sum/intuition.md) |
| Nesting, matching brackets, "most recent first", undo | [Stack](../patterns/stack/intuition.md) |
| Hierarchy, parent and child, "for each node" | [Tree](../patterns/tree/intuition.md) |
| Connectivity, islands, "reachable from", shortest steps on a grid | [Graph](../patterns/graph/intuition.md) |
| Ordering tasks with dependencies, prerequisites | [Topological Sort](../patterns/topological_sort/intuition.md) |
| "Generate all combinations / permutations / subsets" | [Backtracking](../patterns/backtracking_exploration/intuition.md) |
| "Number of ways", "minimum cost", overlapping subproblems | [Dynamic Programming](../patterns/dp_1d_linear/intuition.md) |
| "The k largest / smallest", a running median, merging sorted streams | [Heap](../patterns/heap/intuition.md) |

## When you are stuck

Being stuck is part of the process, not a failure. A few reliable unsticking
moves:

- Solve a smaller version of the problem first, then ask what changes as it
  grows.
- Sort the input and see whether order makes the structure obvious.
- Ask what you would store in a hash map to avoid a repeated search.
- Look at your brute force again and attack the single most wasteful line.

The goal of practice is not to memorize 75 solutions. It is to make these steps
automatic, so that an unfamiliar problem becomes a familiar process.
