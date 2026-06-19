# [Combination Sum](https://leetcode.com/problems/combination-sum/)

**Medium** | **30 minutes** | **Backtracking**

**Pattern:** [Backtracking](../patterns/backtracking_exploration/intuition.md)

**Practice:** [`practice/combination_sum/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/combination_sum/solution.py)

Given an array of **distinct** integers `candidates` and a target integer `target`, return a list of all **unique combinations** of `candidates` where the chosen numbers sum to `target`. You may return the combinations in **any order**.

The **same** number may be chosen from `candidates` an **unlimited number of times**. Two combinations are unique if the frequency of at least one of the chosen numbers is different.

The test cases are generated such that the number of unique combinations that sum up to `target` is less than `150` combinations for the given input.

## Examples

### Example 1

**Input:** `candidates = [2,3,6,7]`, `target = 7`

**Output:** `[[2,2,3],[7]]`

**Explanation:**

```
2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
7 is a candidate, and 7 = 7.
These are the only two combinations.
```

### Example 2

**Input:** `candidates = [2,3,5]`, `target = 8`

**Output:** `[[2,2,2,2],[2,3,3],[3,5]]`

### Example 3

**Input:** `candidates = [2]`, `target = 1`

**Output:** `[]`

## Constraints

- `1 <= candidates.length <= 30`
- `2 <= candidates[i] <= 40`
- All elements of `candidates` are **distinct**.
- `1 <= target <= 40`

## Solutions

### Include-Exclude Backtracking

```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        result: List[List[int]] = []

        def backtrack(index: int, remaining: int, current: List[int]) -> None:
            if remaining == 0:
                result.append(current[:])
                return
            if remaining < 0 or index >= len(candidates):
                return

            # Include candidates[index], staying on the same index to allow reuse.
            current.append(candidates[index])
            backtrack(index, remaining - candidates[index], current)
            current.pop()

            # Exclude candidates[index] and move on to the next candidate.
            backtrack(index + 1, remaining, current)

        backtrack(0, target, [])
        return result
```

#### Approach

The most direct way to think about the problem is a binary decision tree: at each
candidate, we either include it (and stay put so it can be used again) or exclude it
(and move to the next candidate). This frames the search without needing to sort the
input first.

The steps:

1. Recurse with the current `index`, the `remaining` target, and the partial
   `current` combination.
2. If `remaining` reaches `0`, record a copy of `current` as a valid combination.
3. If `remaining` goes negative or we run out of candidates, abandon the branch.
4. Otherwise branch twice: include `candidates[index]` while recursing on the same
   `index` (enabling reuse), then exclude it and recurse on `index + 1`.

Because the "exclude" branch only ever advances the index, no candidate is ever
revisited after we move past it. Each combination is therefore produced exactly once
in the order its candidates first appear, guaranteeing uniqueness.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^target)` (loosely; `O(N^(target / min_candidate))` tighter)

Every node makes a binary choice, so the decision tree has up to `2^target` leaves
in the worst case. A tighter bound is `O(N^(target / m))` where `N` is the number of
candidates and `m` the smallest candidate, since a combination can be at most
`target / m` long. Copying each valid combination adds a factor proportional to its
length.

##### Space Complexity: `O(target / min_candidate)`

Excluding the output, space is dominated by the recursion stack and the `current`
list, both bounded by the maximum combination length `target / min_candidate`.

#### Key Insights

- The include/exclude framing needs no sorting: correctness comes purely from never
  revisiting a candidate on the exclude branch.
- Reuse is captured by recursing on the same `index` in the include branch.
- The `remaining < 0` guard is what stops a branch that has overshot the target.
- Always append a copy (`current[:]`), since `current` is mutated throughout.

### Sorted Backtracking with Pruning

```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        # Sort so we can stop a branch as soon as a candidate overshoots.
        candidates.sort()
        result: List[List[int]] = []

        def backtrack(start: int, remaining: int, current: List[int]) -> None:
            if remaining == 0:
                result.append(current[:])
                return

            for i in range(start, len(candidates)):
                candidate = candidates[i]
                # Sorted order: once one candidate is too big, the rest are too.
                if candidate > remaining:
                    break
                current.append(candidate)
                # Pass i (not i + 1) so the same number may be reused.
                backtrack(i, remaining - candidate, current)
                current.pop()

        backtrack(0, target, [])
        return result
```

#### Approach

This is the same search expressed with a loop rather than a binary tree, plus a
sorting optimization. We explore with the classic "choose, explore, unchoose"
pattern. Two details make it both correct and efficient:

1. Sort `candidates` ascending. This lets us `break` out of the loop the moment a
   candidate exceeds the remaining target, since every later candidate is at least
   as large.
2. Pass the current index `i` (rather than `i + 1`) into the recursive call. This
   allows a number to be reused an unlimited number of times while the `start`
   bound still prevents us from revisiting earlier candidates, which is what avoids
   counting `[2,3]` and `[3,2]` as distinct combinations.

The steps:

1. Sort the candidates.
2. Recurse with a running `remaining` target and the partial `current` combination.
3. When `remaining` hits `0`, record a copy of `current` as a valid combination.
4. For each candidate from `start` onward, prune if it exceeds `remaining`,
   otherwise pick it, recurse allowing reuse, then unpick and continue.

Because we only ever move the start index forward, each combination is generated in
non-decreasing order exactly once, guaranteeing uniqueness.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N^(target / min_candidate))`

Let `N` be the number of candidates and `m` the smallest candidate. The recursion
tree has depth at most `target / m` (the longest a combination can be), and each
node branches up to `N` ways. Copying each valid combination costs an additional
factor proportional to its length. This exponential bound is expected for an
enumeration problem; the sort-and-prune keeps the constant factors low in practice.

##### Space Complexity: `O(target / min_candidate)`

Excluding the output, space is dominated by the recursion stack and the `current`
list, both bounded by the maximum combination length `target / min_candidate`.

#### Key Insights

- Reuse is enabled simply by recursing with `i` instead of `i + 1`; the `start`
  index alone enforces uniqueness without any explicit duplicate filtering.
- Sorting unlocks an early `break`, turning a continue-style skip into a true prune
  that cuts entire subtrees.
- Always append a copy (`current[:]`) of the combination, since `current` is mutated
  throughout the search.
- Since all candidates are positive and distinct, no separate visited set or
  same-level duplicate skip is needed (unlike Combination Sum II).

### Bottom-Up Dynamic Programming

```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        # dp[t] holds every combination summing to t, each in non-decreasing order.
        dp: List[List[List[int]]] = [[] for _ in range(target + 1)]
        dp[0] = [[]]

        for candidate in candidates:
            for t in range(candidate, target + 1):
                for combo in dp[t - candidate]:
                    dp[t].append(combo + [candidate])

        return dp[target]
```

#### Approach

Instead of recursing, we build up answers for every sub-target from `0` to
`target`. The outer loop over candidates (rather than an inner loop) is the trick
that prevents duplicate combinations: by the time we consider a candidate, every
combination already stored uses only earlier candidates, so appending the current
candidate keeps each combination in non-decreasing order and unique.

The steps:

1. Sort the candidates so combinations are built in non-decreasing order.
2. Initialize `dp[0]` with one empty combination; every other `dp[t]` starts empty.
3. For each `candidate`, sweep sub-targets `t` from `candidate` up to `target`.
4. For each combination that sums to `t - candidate`, append `candidate` to form a
   new combination that sums to `t`, and store it in `dp[t]`.
5. Return `dp[target]`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N * target * K)`

For each of `N` candidates and each of up to `target` sub-targets, we copy every
stored combination, where `K` bounds the total number and length of combinations.
Since the result set itself can be exponential, this matches the inherent output
size; the DP adds no asymptotic savings over backtracking for enumeration.

##### Space Complexity: `O(target * K)`

The `dp` table stores, for every sub-target, all combinations reaching it. This is
strictly more memory than backtracking, which only keeps one path plus the output.

#### Key Insights

- Looping over candidates on the outside (and sub-targets on the inside) is what
  enforces non-decreasing order and therefore uniqueness.
- Each `dp[t]` is independent of candidate order within it, so canonicalizing for
  comparison is still required.
- The table makes every intermediate combination explicit, which trades memory for
  the removal of recursion.

## Comparison of Solutions

### Time Complexity

- **Include-Exclude Backtracking**: `O(N^(target / m))` - explores the full
  decision tree without pruning.
- **Sorted Backtracking with Pruning**: `O(N^(target / m))` - same bound, but the
  sorted `break` cuts whole subtrees in practice.
- **Bottom-Up Dynamic Programming**: `O(N * target * K)` - dominated by copying the
  combinations stored per sub-target.

### Space Complexity

- **Include-Exclude Backtracking**: `O(target / m)` - recursion stack plus one path.
- **Sorted Backtracking with Pruning**: `O(target / m)` - recursion stack plus one
  path.
- **Bottom-Up Dynamic Programming**: `O(target * K)` - stores all combinations for
  every sub-target.

### Trade-offs

- **Include-Exclude Backtracking** is the easiest to reason about and needs no
  sorting, but it explores branches that the pruned version would skip.
- **Sorted Backtracking with Pruning** adds an `O(N log N)` sort to gain a strong
  early-exit prune, making it the fastest in practice on real inputs.
- **Bottom-Up Dynamic Programming** removes recursion at the cost of holding every
  intermediate combination in memory, which is rarely worth it here.

### When to Use Each

- **Include-Exclude Backtracking**: When you want the clearest mental model or are
  forbidden from mutating the input by sorting it.
- **Sorted Backtracking with Pruning** (Recommended): The default interview answer;
  cleanest balance of speed and simplicity.
- **Bottom-Up Dynamic Programming**: When sub-target answers are reused elsewhere or
  you specifically want an iterative, stack-free formulation.

### Optimization Notes

- Sorting enables the `if candidate > remaining: break` prune; without sorting you
  could only `continue`, which does not cut subtrees.
- Reuse always comes from staying on the same index (`i` or `index`) in the include
  branch, never from a separate counter.
- All three approaches produce combinations in arbitrary order, so any equality
  check must canonicalize with `sorted(map(sorted, result))`.
