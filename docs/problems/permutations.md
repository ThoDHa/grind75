# [Permutations](https://leetcode.com/problems/permutations/)

**Medium** | **25 minutes** | **Array, Backtracking**

**Pattern:** [Backtracking](../patterns/backtracking_exploration/intuition.md)

**Practice:** [`practice/permutations/solution.py`](../../practice/permutations/solution.py)

Given an array `nums` of distinct integers, return all the possible permutations. You can return the answer in any order.

## Examples

### Example 1

**Input:** `nums = [1,2,3]`

**Output:** `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`

### Example 2

**Input:** `nums = [0,1]`

**Output:** `[[0,1],[1,0]]`

### Example 3

**Input:** `nums = [1]`

**Output:** `[[1]]`

## Constraints

- `1 <= nums.length <= 6`
- `-10 <= nums[i] <= 10`
- All the integers of `nums` are unique.

## Solutions

### Backtracking with Path Building

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result: List[List[int]] = []

        def backtrack(current: List[int]) -> None:
            if len(current) == len(nums):
                result.append(current[:])
                return
            for num in nums:
                if num not in current:
                    current.append(num)
                    backtrack(current)
                    current.pop()

        backtrack([])
        return result
```

#### Approach

This is the classic backtracking template applied directly: build one permutation element by element, and at each position try every number that has not been placed yet. The recursion follows the choose, explore, unchoose pattern.

1. Maintain a `current` list holding the partial permutation under construction.
2. When `current` reaches the length of `nums`, a complete permutation has been formed, so append a copy to `result`.
3. Otherwise, iterate over `nums` and skip any number already present in `current`.
4. Choose a number by appending it, explore by recursing, then unchoose by popping it so the next iteration starts from a clean slate.

The decision tree has `n!` leaves, one per permutation; each root-to-leaf path corresponds to one ordering of the input.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! × n)`

There are `n!` permutations to generate. Each completed permutation costs `O(n)` to copy into the result. The `num not in current` membership scan is also `O(n)`, but it does not change the asymptotic bound that is already dominated by the `n!` leaf count times the `O(n)` work per leaf.

##### Space Complexity: `O(n)`

The recursion depth is at most `n`, and `current` holds at most `n` elements. The output itself is not counted toward auxiliary space.

#### Key Insights

- The choose, explore, unchoose template is the most narratable backtracking pattern and extends naturally to subsets, combinations, and permutations with duplicates.
- Appending `current[:]` rather than `current` is essential; storing the live reference would let later mutations corrupt results already saved.
- The `num not in current` guard keeps the code short and readable, trading an `O(n)` scan for not having to track a separate used structure.

### Backtracking with Used Array

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result: List[List[int]] = []
        n = len(nums)
        path: List[int] = []
        used = [False] * n

        def backtrack() -> None:
            if len(path) == n:
                result.append(path[:])
                return
            for i in range(n):
                if used[i]:
                    continue
                path.append(nums[i])
                used[i] = True
                backtrack()
                path.pop()
                used[i] = False

        backtrack()
        return result
```

#### Approach

This refines the path-building idea by replacing the `O(n)` membership test with an `O(1)` boolean lookup. A `used` array records, by index, which elements are already placed in the current `path`.

1. Keep a `path` list for the partial permutation and a `used` boolean array parallel to `nums`.
2. When `path` is full, append a copy to `result`.
3. For each index `i`, skip it when `used[i]` is `True`; otherwise place `nums[i]`.
4. Mark `used[i] = True` before recursing and reset it to `False` afterward to restore state.

Indexing by position rather than value also keeps the approach correct if the problem were later relaxed to allow duplicate values.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! × n)`

The algorithm still visits `n!` leaves and copies an `n`-element permutation at each one. The constant `O(1)` `used` lookup removes the linear membership scan, improving the constant factor without changing the asymptotic bound.

##### Space Complexity: `O(n)`

The recursion stack, the `path`, and the `used` array are each `O(n)`. Output space is not counted.

#### Key Insights

- Tracking usage by index with an `O(1)` boolean lookup is strictly faster than the `O(n)` `num not in current` scan.
- Indexing by position rather than value generalizes cleanly to inputs that contain duplicates.
- The recursion remains shallow, bounded by `n`, so stack usage is never a concern within the constraints.

### Backtracking with Index Swapping

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result: List[List[int]] = []
        n = len(nums)

        def backtrack(start: int) -> None:
            if start == n:
                result.append(nums[:])
                return
            for i in range(start, n):
                nums[start], nums[i] = nums[i], nums[start]
                backtrack(start + 1)
                nums[start], nums[i] = nums[i], nums[start]

        backtrack(0)
        return result
```

#### Approach

Instead of carrying a separate `path` and `used` array, this approach permutes `nums` in place. The array is partitioned so that `nums[0..start-1]` are fixed prefix positions and `nums[start..n-1]` are the remaining candidates for position `start`.

1. When `start` reaches `n`, every position is fixed, so append a copy of `nums`.
2. For each `i` from `start` to `n - 1`, swap `nums[i]` into position `start`.
3. Recurse on `start + 1` to fix the next position.
4. Swap back to restore the array before trying the next candidate.

The partition itself plays the role of the `used` array, which is why no auxiliary tracking structure is needed.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! × n)`

The recursion produces `n!` complete arrangements, and copying each `n`-element arrangement into the result costs `O(n)`.

##### Space Complexity: `O(n)`

Only the recursion stack, bounded by `n`, is used beyond the output. There is no extra `path` or `used` allocation per call.

#### Key Insights

- The fixed-prefix partition encodes which elements are still available, eliminating the `used` array entirely.
- The approach mutates the input array; the symmetric swap-back is what keeps state consistent across sibling recursive calls.
- It is the most space-frugal backtracking variant here, at the cost of being the least obvious to read.

### Iterative Build-Up

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = [[]]
        for num in nums:
            new_result = []
            for perm in result:
                for i in range(len(perm) + 1):
                    new_result.append(perm[:i] + [num] + perm[i:])
            result = new_result
        return result
```

#### Approach

This non-recursive approach builds the full set of permutations by repeated insertion. Starting from the single empty permutation, each new number is inserted at every possible position of every permutation gathered so far.

1. Seed `result` with one empty permutation, `[[]]`.
2. For each `num` in `nums`, create an empty `new_result`.
3. For every existing permutation, insert `num` at each of its `len(perm) + 1` positions, appending each result to `new_result`.
4. Replace `result` with `new_result` and continue.

For example, with `[1,2,3]`: start `[[]]`, add `1` to get `[[1]]`, add `2` to get `[[2,1],[1,2]]`, then add `3` to expand each of those into three new permutations.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! × n)`

After processing `k` numbers there are `k!` permutations, and inserting the next number creates `k + 1` new lists per permutation, each costing `O(k)` to build by slicing. Summed across all rounds the work is dominated by the final `O(n! × n)` term.

##### Space Complexity: `O(n! × n)`

Each round holds the full set of permutations built so far, and the final round materializes all `n!` permutations of length `n` simultaneously.

#### Key Insights

- Permutations can be generated bottom-up without recursion, which avoids any call-stack depth concern.
- The insertion trick is correct because inserting one new element at every position of every shorter permutation enumerates each longer permutation exactly once.
- The tradeoff is memory: unlike the backtracking variants, every intermediate generation is held in full.

### Built-in itertools.permutations

```python
from itertools import permutations

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        return [list(perm) for perm in permutations(nums)]
```

#### Approach

Python's `itertools.permutations` generates every ordering of the input. Each yielded item is a tuple, so the comprehension converts them to lists to match the expected return type.

1. Call `permutations(nums)` to obtain an iterator over all orderings as tuples.
2. Convert each tuple to a list and collect them into the result.

This is the most concise option but is generally not acceptable in interviews, since it hides the algorithm the question is asking you to demonstrate.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! × n)`

The library produces `n!` tuples, and converting each `n`-length tuple to a list costs `O(n)`. The asymptotic bound matches the hand-written approaches, with smaller constant factors from the C implementation.

##### Space Complexity: `O(n! × n)`

The returned list stores all `n!` permutations of length `n`. The generator itself uses only `O(n)` internal state.

#### Key Insights

- The standard library does the core work, so this is ranked last despite being the shortest.
- It is ideal for production code where conciseness and constant-factor speed matter more than demonstrating the algorithm.
- Remembering to convert tuples to lists is the only real subtlety.

## Comparison of Solutions

### Time Complexity

- **Backtracking with Path Building**: `O(n! × n)` - `n!` permutations, each `O(n)` to copy, with an additional `O(n)` membership scan that does not change the bound.
- **Backtracking with Used Array**: `O(n! × n)` - same leaf count and copy cost, with the membership scan replaced by an `O(1)` lookup.
- **Backtracking with Index Swapping**: `O(n! × n)` - `n!` arrangements, each `O(n)` to copy.
- **Iterative Build-Up**: `O(n! × n)` - each round inserts the next number into every existing permutation, dominated by the final `O(n! × n)` term.
- **Built-in itertools.permutations**: `O(n! × n)` - same theoretical bound with optimized C constant factors.

### Space Complexity

- **Backtracking with Path Building**: `O(n)` - recursion stack plus the `current` path.
- **Backtracking with Used Array**: `O(n)` - recursion stack, `path`, and `used` array.
- **Backtracking with Index Swapping**: `O(n)` - recursion stack only, with no auxiliary tracking.
- **Iterative Build-Up**: `O(n! × n)` - holds every intermediate generation of permutations in full.
- **Built-in itertools.permutations**: `O(n! × n)` - for storing the result; the generator uses `O(n)` internal state.

### Trade-offs

- **Backtracking with Path Building**: Clearest to narrate and extends to duplicates, at the cost of an `O(n)` membership scan per choice.
- **Backtracking with Used Array**: Removes the membership scan with an `O(1)` lookup, adding one small auxiliary array.
- **Backtracking with Index Swapping**: The most space-frugal variant, but it mutates the input and is the least intuitive to read.
- **Iterative Build-Up**: Recursion-free and easy to reason about, but it holds every intermediate generation in memory.
- **Built-in itertools.permutations**: Concise and fast, but hides the algorithm and is unsuitable for interviews.

### When to Use Each

- **Backtracking with Path Building** (recommended): Best for interviews and learning. The choose, explore, unchoose template is the clearest to explain.
- **Backtracking with Used Array**: When you want the same clarity with a better constant factor, or anticipate generalizing to duplicate values.
- **Backtracking with Index Swapping**: When space is at a premium and mutating the input array is acceptable.
- **Iterative Build-Up**: When a non-recursive construction is preferred and the extra intermediate memory is acceptable.
- **Built-in itertools.permutations**: For production code where performance and conciseness matter more than demonstrating algorithmic knowledge.

### Optimization Notes

- Since every approach shares the `O(n! × n)` time floor, optimization here is about space and clarity rather than asymptotic speed.
- The path-building membership scan is the one avoidable cost: swapping it for an indexed `used` array turns an `O(n)` check into `O(1)`.
- When mutating the input is acceptable, the index-swapping approach removes the per-call `path` allocation entirely.
- A key pitfall across the backtracking variants is appending the live working list instead of a copy; always append `path[:]` or `current[:]` so later mutations do not corrupt stored results.
