# [Problem Title](https://leetcode.com/problems/problem-slug/)

**Easy | Medium | Hard** | **NN minutes** | **Category, Category**

<!--
One to three short paragraphs restating the problem in plain prose. Keep the
wording close to LeetCode's, wrapping at a comfortable line width. Use `inline
code` for variable names and literal values.
-->

## Examples

### Example 1

**Input:** `arg = value`, `arg2 = value`

**Output:** `value`

**Explanation:** Why this output follows from the input. Use `inline code` for
values. Omit this line when the mapping is self-evident.

### Example 2

**Input:** `arg = value`

**Output:** `value`

## Constraints

- `1 <= n <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
- One bullet per constraint, copied from the problem.

## Follow-up

<!-- Optional. Include only when the problem poses a follow-up question. -->

Can you come up with an algorithm that beats the obvious approach?

## Solutions

<!--
==============================================================================
SOLUTION CONVENTIONS (apply to every problem):

NAMING
  - Name each solution by its approach. Use the established algorithm name when
    one exists (Kadane's Algorithm, Boyer-Moore Voting, Dutch National Flag,
    Floyd's Cycle Detection, Morris Traversal), otherwise a clean technique name
    (Brute Force, Hash Map, Two Pointers, Sliding Window, Recursive DFS,
    Iterative BFS, Bottom-Up DP, Top-Down Memoization, Monotonic Stack, Sorting).
  - Never number solutions (no "### Solution 1"). Order alone conveys sequence.
  - No editorializing parenthetical qualifiers: avoid "(Optimal)", "(Educational)",
    "(Alternative)", "(Pythonic)", "(Most Common)", "(Hand-Written)", and the
    "Dynamic Programming (Subset-Sum Table)" style. ("(Recommended)" is fine
    inside a When-to-Use bullet, which is not a header.)

ORDERING (by discoverability, not raw speed)
  - The first solution is the most intuitive / self-derivable one: brute force,
    direct simulation, an obvious hashmap/set/sort written out by hand, or a
    plain DFS/BFS.
  - Later solutions are progressively more specialized: named algorithms and
    clever tricks you would have to learn or look up. The optimal solution
    usually lands last among the from-scratch approaches.
  - PYTHONIC ONE-LINERS GO LAST, after every from-scratch approach, even when
    they look trivially simple. A solution that leans on a built-in or stdlib
    call to do the core work (`sorted(s) == sorted(t)`, `Counter(a) == Counter(b)`,
    `len(set(x)) < len(x)`, `itertools.permutations`, `int(s, 2)` / `bin`, `re`)
    is ranked by what the language does for you, not by how short it reads. When
    several such shortcuts exist, the most library-driven one is last of all.

LIBRARY-FREE REQUIREMENT
  - If a solution leans on a library to do the CORE work (Counter, heapq, bisect,
    itertools, OrderedDict, re, math), the file must ALSO include a from-scratch,
    library-free solution (hand-written binary search instead of bisect,
    hashmap + doubly linked list instead of OrderedDict, a 26-int count array
    instead of Counter). The idiomatic containers `deque` and `defaultdict` do
    NOT count as "the library doing the work" and may be used freely.

CODE
  - LeetCode style: `class Solution`, type hints, no Python 2 `(object)`. Keep
    code correct and verified against the examples.

==============================================================================
CHOOSE ONE LAYOUT:

  A) SINGLE SOLUTION   - one approach. Keep the one named `### <Name>` block
                         below, delete the multi-solution block AND the
                         `## Comparison of Solutions` section.

  B) MULTIPLE SOLUTIONS - two or more approaches. Delete the single-solution
                          block, keep one named `### <Name>` block per solution,
                          and keep the `## Comparison of Solutions` section.
==============================================================================
-->

<!-- ----------------------------- LAYOUT A ----------------------------- -->

### Hash Map

```python
class Solution:
    def method(self, ...) -> ...:
        # implementation
        ...
```

#### Approach

Prose describing the idea, followed by the concrete steps:

1. First step.
2. Second step.
3. Third step.

Optional closing paragraph on why the approach is correct.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Why the time bound holds.

##### Space Complexity: `O(1)`

Why the space bound holds.

#### Key Insights

- The non-obvious observation that makes the solution work.
- A tradeoff or edge case the approach handles cleanly.
- A pitfall avoided.

<!-- --------------------------- END LAYOUT A --------------------------- -->

<!-- ----------------------------- LAYOUT B ----------------------------- -->

### Brute Force

```python
class Solution:
    def method(self, ...) -> ...:
        # implementation
        ...
```

#### Approach

Prose plus numbered steps:

1. First step.
2. Second step.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Why the time bound holds.

##### Space Complexity: `O(1)`

Why the space bound holds.

#### Key Insights

- Insight specific to this approach.
- Why it is simple but limited.

### Hash Map

```python
class Solution:
    def method(self, ...) -> ...:
        # implementation
        ...
```

#### Approach

Prose plus numbered steps.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Why the time bound holds.

##### Space Complexity: `O(n)`

Why the space bound holds.

#### Key Insights

- Insight specific to this approach.
- The space-time tradeoff it represents.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - one-line reason.
- **Hash Map**: `O(n)` - one-line reason.

### Space Complexity

- **Brute Force**: `O(1)` - one-line reason.
- **Hash Map**: `O(n)` - one-line reason.

### Trade-offs

- What the Brute Force approach gives up and gains.
- What the Hash Map approach gives up and gains.

### When to Use Each

- **Brute Force**: The situation where it is the right call.
- **Hash Map**: The situation where it is the right call.

### Optimization Notes

- Implementation detail worth highlighting (for example, computing `mid` as
  `left + (right - left) // 2` to avoid overflow).
- Production considerations.

<!-- --------------------------- END LAYOUT B --------------------------- -->
