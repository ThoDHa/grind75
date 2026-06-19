# Algorithm Pattern Intuition Guides

These guides explain the *why* behind each algorithm pattern: the mental models, invariants, and decision frameworks that make them work. Understanding patterns is the key to solving unfamiliar problems.

## Array & Sequences

| Pattern | Key Concept | Grind75 Problems |
|---------|-------------|------------------|
| [Sliding Window](sliding_window/intuition.md) | Moving frame of attention over contiguous sequences | Longest Substring w/o Repeats, Find All Anagrams, Minimum Window Substring |
| [Two Pointers](two_pointers/intuition.md) | Coordinated pointers that shrink the search space | Valid Palindrome, 3Sum, Container With Most Water, Sort Colors |
| [Prefix Sum](prefix_sum/intuition.md) | Precomputed cumulative sums for range queries | Product of Array Except Self, Maximum Subarray |
| [Monotonic Stack](monotonic_stack/intuition.md) | Maintaining ordered elements for boundary problems | Trapping Rain Water, Largest Rectangle in Histogram |

## Search

| Pattern | Key Concept | Grind75 Problems |
|---------|-------------|------------------|
| [Binary Search](binary_search/intuition.md) | Halving the search space with monotonic properties | Binary Search, First Bad Version, Search Rotated Array, Time Based KV |

## Trees & Graphs

| Pattern | Key Concept | Grind75 Problems |
|---------|-------------|------------------|
| [Tree Traversal](tree/intuition.md) | DFS and BFS strategies for hierarchical data | Invert Tree, Max Depth, Level Order, Validate BST, LCA, Right Side View, Construct Tree |
| [Tree DP](tree_dp/intuition.md) | Recursive DP on tree structures | Diameter of Binary Tree, Max Path Sum |
| [Graph Traversal](graph/intuition.md) | DFS/BFS for connectivity and distance | Flood Fill, Clone Graph, Number of Islands, Word Search, Course Schedule |
| [Topological Sort](topological_sort/intuition.md) | Ordering nodes by dependencies | Course Schedule, Minimum Height Trees |
| [Shortest Path](shortest_path/intuition.md) | Dijkstra, BFS, and beyond for weighted graphs | Word Ladder |
| [Multi-Source BFS](grid_bfs_multi_source/intuition.md) | BFS from multiple starting points on grids | 01 Matrix, Rotting Oranges |
| [Union-Find](union_find/intuition.md) | Disjoint set connectivity tracking | Accounts Merge |

## Heaps & Intervals

| Pattern | Key Concept | Grind75 Problems |
|---------|-------------|------------------|
| [Heap / Priority Queue](heap/intuition.md) | Efficient extreme-element access | K Closest Points, Task Scheduler, Find Median, Merge k Sorted Lists |
| [Interval](interval/intuition.md) | Merging and scheduling overlapping ranges | Insert Interval, Merge Intervals |

## Dynamic Programming

| Pattern | Key Concept | Grind75 Problems |
|---------|-------------|------------------|
| [DP 1D Linear](dp_1d_linear/intuition.md) | Single-array DP with linear recurrence | Climbing Stairs, Buy/Sell Stock, Maximum Subarray, Word Break |
| [DP Knapsack/Subset](dp_knapsack_subset/intuition.md) | Subset sum and bounded/unbounded knapsack | Coin Change, Partition Equal Subset Sum |
| [String DP](string_dp/intuition.md) | DP for string alignment and palindromes | Longest Palindromic Substring |

## Advanced Patterns

| Pattern | Key Concept | Grind75 Problems |
|---------|-------------|------------------|
| [Backtracking](backtracking_exploration/intuition.md) | Exhaustive search with pruning | Combination Sum, Permutations, Subsets, Letter Combinations, Word Search |
| [Trie](trie/intuition.md) | Prefix tree for efficient string lookups | Implement Trie, Word Break |
| [Greedy](greedy_core/intuition.md) | Locally optimal choices that lead to global optimum | Task Scheduler |
| [K-Way Merge](k_way_merge/intuition.md) | Merging multiple sorted sequences | Merge Two Sorted Lists, Merge k Sorted Lists |
| [Linked List Reversal](linked_list_in_place_reversal/intuition.md) | In-place linked list restructuring | Reverse Linked List |

---

*Pattern intuition guides adapted from [NeetCode Practice Framework](https://lufftw.github.io/neetcode/).*
