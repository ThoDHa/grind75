# Algorithm Pattern Intuition Guides

These guides explain the *why* behind each algorithm pattern: the mental models, invariants, and decision frameworks that make them work. Understanding patterns is the key to solving unfamiliar problems.

## Suggested Reading Order

The seven groups double as a curriculum: later guides lean on the invariants of earlier ones. Read the groups roughly in this order; within a group, the table order is a sensible reading order.

1. **Fundamentals**: Hashing & Frequency Counting, String, Stack, Simulation, Data-Structure Design. No prerequisites: this is the floor everything else stands on. The String guide doubles as a routing map and can be read here as a preview or revisited at any point.
2. **Array & Sequences**: Sliding Window, Two Pointers, Prefix Sum, Monotonic Stack. Prerequisites: Hashing (sliding windows keep their state in a hash map) and Stack (Monotonic Stack is the stack with an ordering discipline).
3. **Search**: Binary Search. Prerequisite: none strictly; Two Pointers warm up the ordered-input elimination instinct, and the [Big-O page](../foundations/big_o.md) explains why sorted input is worth paying for.
4. **Trees & Graphs**: Tree Traversal, Tree DP, Graph Traversal, Topological Sort, Shortest Path, Multi-Source BFS, Union-Find. Prerequisites: [Recursion and the Call Stack](../foundations/recursion.md) first, then Tree Traversal before Tree DP, and Graph Traversal before Topological Sort, Shortest Path, and Multi-Source BFS. Tree DP also draws on DP 1D Linear (group 6): read that first, or return to Tree DP after it.
5. **Heaps & Intervals**: Heap / Priority Queue, Interval. No prerequisites.
6. **Dynamic Programming**: DP 1D Linear, DP Knapsack/Subset, String DP, Grid DP. Prerequisites: [Recursion](../foundations/recursion.md), then DP 1D Linear before Grid DP (the same skill on a second axis) and before String DP.
7. **Advanced Patterns**: Backtracking, Trie, Greedy, K-Way Merge, Linked List Reversal. Prerequisites: Backtracking wants Recursion plus the traversal mindset from Graph Traversal; K-Way Merge wants Heap. Linked List Reversal (with its fast/slow pointers section) is self-contained: the [linked-list pictures](../foundations/data_structures.md#linked-list) are enough, so it can be pulled earlier if wanted.

## Fundamentals

| Pattern | Key Concept | Grind75 Problems |
|---------|-------------|------------------|
| [Hashing & Frequency Counting](hashing/intuition.md) | Trading space for O(1) lookup, membership, and counting | Two Sum, Valid Anagram, Contains Duplicate, Ransom Note, Longest Palindrome, Majority Element |
| [String](string/intuition.md) | A routing map: every string question is counting, framing, two ends, alignment, or parsing | Valid Palindrome, Valid Anagram, Longest Palindrome, Longest Substring w/o Repeats, Find All Anagrams, Minimum Window Substring |
| [Stack](stack/intuition.md) | LIFO processing for nesting, matching, and expression evaluation | Valid Parentheses, Evaluate RPN, Basic Calculator |
| [Simulation](simulation/intuition.md) | Modeling a described process directly, with care for boundaries and edge cases | Spiral Matrix, Add Binary, String to Integer (atoi) |
| [Data-Structure Design](design/intuition.md) | Composing primitive structures to meet operation complexity guarantees | Min Stack, Implement Queue using Stacks, LRU Cache, Maximum Frequency Stack |

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
| [Grid DP](grid_dp/intuition.md) | 2D DP on a grid, each cell built from its neighbors | Unique Paths |

## Advanced Patterns

| Pattern | Key Concept | Grind75 Problems |
|---------|-------------|------------------|
| [Backtracking](backtracking_exploration/intuition.md) | Exhaustive search with pruning | Combination Sum, Permutations, Subsets, Letter Combinations, Word Search |
| [Trie](trie/intuition.md) | Prefix tree for efficient string lookups | Implement Trie, Word Break |
| [Greedy](greedy_core/intuition.md) | Locally optimal choices that lead to global optimum | Task Scheduler |
| [K-Way Merge](k_way_merge/intuition.md) | Merging multiple sorted sequences | Merge Two Sorted Lists, Merge k Sorted Lists |
| [Linked List Reversal](linked_list_in_place_reversal/intuition.md) | In-place linked list restructuring; fast/slow pointers for cycle detection and midpoints | Reverse Linked List, Linked List Cycle, Middle of the Linked List |

---

## Where the TIH Topics Live Here

The [Tech Interview Handbook](https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/) (TIH) organizes interview algorithms into 18 topics, each rated by priority. The table maps every TIH topic to its home here; data-structure-flavored topics also point at the picture-level intros in [Data Structures in Pictures](../foundations/data_structures.md).

| TIH topic | TIH priority | Where it lives here |
|-----------|--------------|---------------------|
| Array | High | [Sliding Window](sliding_window/intuition.md), [Two Pointers](two_pointers/intuition.md), [Prefix Sum](prefix_sum/intuition.md), [Monotonic Stack](monotonic_stack/intuition.md); intro: [Array](../foundations/data_structures.md#array-list) |
| String | High | [String](string/intuition.md), which routes into [Hashing](hashing/intuition.md), [Sliding Window](sliding_window/intuition.md), [Two Pointers](two_pointers/intuition.md), and [String DP](string_dp/intuition.md) |
| Hash table | Mid | [Hashing & Frequency Counting](hashing/intuition.md); intro: [Hash map](../foundations/data_structures.md#hash-map-dictionary-and-hash-set) |
| Recursion | Mid | [Recursion and the Call Stack](../foundations/recursion.md); applied in [Backtracking](backtracking_exploration/intuition.md) |
| Sorting and searching | High | [Binary Search](binary_search/intuition.md); sorting costs on the [Big-O page](../foundations/big_o.md) |
| Matrix | High | [Multi-Source BFS](grid_bfs_multi_source/intuition.md), [Grid DP](grid_dp/intuition.md), [Simulation](simulation/intuition.md); grids are arrays of arrays: [Array](../foundations/data_structures.md#array-list) |
| Linked list | Mid | [Linked List Reversal](linked_list_in_place_reversal/intuition.md) (including fast/slow pointers), [K-Way Merge](k_way_merge/intuition.md); intro: [Linked list](../foundations/data_structures.md#linked-list) |
| Queue | Mid | [Data-Structure Design](design/intuition.md) (Implement Queue using Stacks); intro: [Queue](../foundations/data_structures.md#queue) |
| Stack | Mid | [Stack](stack/intuition.md), [Monotonic Stack](monotonic_stack/intuition.md); intro: [Stack](../foundations/data_structures.md#stack) |
| Interval | Mid | [Interval](interval/intuition.md) |
| Tree | High | [Tree](tree/intuition.md), [Tree DP](tree_dp/intuition.md); intro: [Tree](../foundations/data_structures.md#tree) |
| Graph | High | [Graph](graph/intuition.md), [Topological Sort](topological_sort/intuition.md), [Shortest Path](shortest_path/intuition.md), [Multi-Source BFS](grid_bfs_multi_source/intuition.md), [Union-Find](union_find/intuition.md); intro: [Graph](../foundations/data_structures.md#graph) |
| Heap | Mid | [Heap / Priority Queue](heap/intuition.md), [K-Way Merge](k_way_merge/intuition.md); intro: [Heap](../foundations/data_structures.md#heap-priority-queue) |
| Trie | Mid | [Trie](trie/intuition.md); intro: [Trie](../foundations/data_structures.md#trie-prefix-tree) |
| Dynamic programming | Low | [DP 1D Linear](dp_1d_linear/intuition.md), [DP Knapsack/Subset](dp_knapsack_subset/intuition.md), [String DP](string_dp/intuition.md), [Grid DP](grid_dp/intuition.md), [Tree DP](tree_dp/intuition.md) |
| Binary | Low | Not covered yet (no bit-manipulation guide) |
| Math | Low | Not covered yet |
| Geometry | Low | Not covered yet |

The reverse direction is not total: several of our guides (Monotonic Stack, Union-Find, Greedy, Simulation, Data-Structure Design) have no TIH topic of their own; TIH buries them inside broader topics or omits them.

---

*Most pattern intuition guides are adapted from the [NeetCode Practice Framework](https://lufftw.github.io/neetcode/). The Fundamentals guides (Hashing & Frequency Counting, Stack, Simulation, Data-Structure Design, String) and Grid DP are original to this project. Corner-case checklists in the guides are adapted from the [Tech Interview Handbook](https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/) algorithm cheatsheets (MIT licensed), with the edges re-derived per pattern.*
