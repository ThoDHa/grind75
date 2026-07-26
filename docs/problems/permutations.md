# [Permutations](https://leetcode.com/problems/permutations/)

**Medium** | **25 minutes** | **Array, Backtracking**

**Pattern:** [Backtracking](../patterns/backtracking_exploration/intuition.md)

**Algorithm:** [Backtracking](https://en.wikipedia.org/wiki/Backtracking) · [Permutation](https://en.wikipedia.org/wiki/Permutation) · [Heap's algorithm](https://en.wikipedia.org/wiki/Heap%27s_algorithm)

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
from typing import List


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

#### Formula

Each position consumes one unused number, so the branching factor shrinks by one
at every depth. The leaf count is the [factorial](https://en.wikipedia.org/wiki/Factorial):

$$
n \times (n-1) \times \dots \times 1 = n!
$$

```text
n * (n - 1) * ... * 1 = n!
```

The recursion tree is wider than its leaf count suggests. At depth `k` there is
one node per ordered arrangement of `k` distinct elements, so the total node
count is:

$$
\sum_{k=0}^{n} \frac{n!}{(n-k)!} \ = \ n! \sum_{j=0}^{n} \frac{1}{j!} \ \approx \ e \cdot n!
$$

```text
sum over k = 0 to n of n! / (n - k)!
    = n! * (sum over j = 0 to n of 1 / j!)
    approximately e * n!
```

The interior nodes only add a constant factor of about \(e \approx 2.718\) over
the \(n!\) leaves, which is why the bound is quoted as \(O(n! \times n)\): the
tree's shape contributes nothing asymptotically, and the \(n\) comes from copying
each finished permutation.

#### Approach

This is the classic [backtracking](https://en.wikipedia.org/wiki/Backtracking) template applied directly: build one permutation element by element, and at each position try every number that has not been placed yet. The recursion follows the choose, explore, unchoose pattern.

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

#### Walkthrough

Let us watch this first solution run on Example 1, `nums = [1,2,3]`. The trace below is an indented call tree: each line is one `backtrack(current)` call, showing the value of `current` when that call begins. Indentation marks recursion depth. A call iterates `num` over `1, 2, 3` in order, skips any `num` already in `current`, and for each survivor it appends, recurses, then pops (the choose, explore, unchoose cycle). When `current` reaches length `3`, a copy is appended to `result`.

```text
backtrack([])
├─ choose 1 -> backtrack([1])
│  ├─ choose 2 -> backtrack([1,2])
│  │  └─ choose 3 -> backtrack([1,2,3])  -> length 3, append [1,2,3]
│  └─ choose 3 -> backtrack([1,3])
│     └─ choose 2 -> backtrack([1,3,2])  -> length 3, append [1,3,2]
├─ choose 2 -> backtrack([2])
│  ├─ choose 1 -> backtrack([2,1])
│  │  └─ choose 3 -> backtrack([2,1,3])  -> length 3, append [2,1,3]
│  └─ choose 3 -> backtrack([2,3])
│     └─ choose 1 -> backtrack([2,3,1])  -> length 3, append [2,3,1]
└─ choose 3 -> backtrack([3])
   ├─ choose 1 -> backtrack([3,1])
   │  └─ choose 2 -> backtrack([3,1,2])  -> length 3, append [3,1,2]
   └─ choose 2 -> backtrack([3,2])
      └─ choose 1 -> backtrack([3,2,1])  -> length 3, append [3,2,1]
```

Reading one branch end to end: `backtrack([])` first appends `1`, recurses into `backtrack([1])`, which appends `2` and recurses into `backtrack([1,2])`, which appends `3` to reach `[1,2,3]`. That call sees `len(current) == 3`, so it appends a copy and returns. Control unwinds: `backtrack([1,2])` pops `3` and has no more numbers to try, so it returns; `backtrack([1])` pops `2`, then tries `3` next, producing `[1,3,2]`. The same unwind-and-retry repeats across the `2` and `3` branches.

Appending in iteration order, `result` fills as `[1,2,3]`, then `[1,3,2]`, `[2,1,3]`, `[2,3,1]`, `[3,1,2]`, and finally `[3,2,1]`. The returned value is `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`, which matches the expected Output for Example 1.

### Backtracking with Used Array

```python
from typing import List


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
from typing import List


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
from typing import List


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

This non-recursive approach builds the full set of [permutations](https://en.wikipedia.org/wiki/Permutation) by repeated insertion. Starting from the single empty permutation, each new number is inserted at every possible position of every permutation gathered so far.

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

### Heap's Algorithm

```python
from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result: List[List[int]] = []

        def generate(k: int) -> None:
            if k == 1:
                result.append(nums[:])
                return
            for i in range(k):
                generate(k - 1)
                if i < k - 1:
                    if k % 2 == 0:
                        nums[i], nums[k - 1] = nums[k - 1], nums[i]
                    else:
                        nums[0], nums[k - 1] = nums[k - 1], nums[0]

        generate(len(nums))
        return result
```

#### Approach

This is the classic [minimal-change permutation generator](https://en.wikipedia.org/wiki/Heap%27s_algorithm) published by B. R. Heap in 1963. The name refers to its author and has nothing to do with the heap data structure: no priority queue or heap property appears anywhere in the algorithm. Its defining property is that each permutation is produced from the previous one by a single swap of two elements, whereas the backtracking approaches rebuild a path prefix between outputs.

1. `generate(k)` emits every permutation of the first `k` positions of `nums` while leaving `nums[k..n-1]` untouched.
2. When `k == 1`, the arrangement is fully determined, so snapshot `nums[:]` into `result`.
3. Otherwise run `k` rounds: each round recurses with `generate(k - 1)`, then performs exactly one swap to move a fresh element into position `k - 1` before the next round. No swap follows the final round.
4. The swap is parity-dependent: when `k` is even, swap `nums[i]` (the loop index) with `nums[k - 1]`; when `k` is odd, always swap `nums[0]` with `nums[k - 1]`.

The parity rule is the subtle heart of the algorithm. The recursive calls leave the first `k - 1` elements rearranged in a way that depends on whether `k - 1` is even or odd, and the two swap choices are calibrated to that behavior: an inductive argument shows each choice moves an element that has not yet occupied position `k - 1` into that slot, so every element takes the last position exactly once across the `k` rounds. On `nums = [1,2,3]` the emission order is `[1,2,3]`, `[2,1,3]`, `[3,1,2]`, `[1,3,2]`, `[2,3,1]`, `[3,2,1]`; note that every adjacent pair differs by exactly one transposition.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! × n)`

There are `n!` permutations, and snapshotting each `n`-element arrangement costs `O(n)`. The generation machinery itself is cheaper than that: only one swap separates consecutive permutations, so the swap work amortizes to `O(1)` per permutation, and the total is dominated by the mandatory copy at each leaf.

##### Space Complexity: `O(n)`

The recursion depth is `n`, and the algorithm permutes `nums` in place with no auxiliary tracking structures. Output space is not counted.

#### Key Insights

- Heap's algorithm is a minimal-change enumeration: consecutive outputs differ by a single transposition, the permutation analogue of a Gray code, which is why the generation work amortizes to `O(1)` swaps per permutation.
- That property makes it a systems and CS-classics tool more than an interview answer: it shines when a consumer can update its state incrementally after one swap (re-evaluating a cost function over the arrangement, exhaustive testing over orderings) instead of materializing every output. Sedgewick's classic survey of permutation generation methods singled it out as among the most efficient. In an interview, backtracking is the expected demonstration.
- Its emission order differs from the backtracking approaches' order, and that is fine here: the problem accepts any order, and the practice tests canonicalize by sorting the outer list of permutations before comparing.
- Like the index-swapping approach, it mutates the input array, and it does not restore the original order when it finishes.

### Built-in itertools.permutations

```python
from typing import List


from itertools import permutations

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        return [list(perm) for perm in permutations(nums)]
```

#### Approach

Python's [`itertools.permutations`](https://docs.python.org/3/library/itertools.html) generates every ordering of the input. Each yielded item is a tuple, so the comprehension converts them to lists to match the expected return type.

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
- **Heap's Algorithm**: `O(n! × n)` - one swap per new permutation amortizes to `O(1)` generation work; the `O(n)` snapshot per output dominates.
- **Built-in itertools.permutations**: `O(n! × n)` - same theoretical bound with optimized C constant factors.

### Space Complexity

- **Backtracking with Path Building**: `O(n)` - recursion stack plus the `current` path.
- **Backtracking with Used Array**: `O(n)` - recursion stack, `path`, and `used` array.
- **Backtracking with Index Swapping**: `O(n)` - recursion stack only, with no auxiliary tracking.
- **Iterative Build-Up**: `O(n! × n)` - holds every intermediate generation of permutations in full.
- **Heap's Algorithm**: `O(n)` - recursion stack only; permutations are generated in place with no auxiliary tracking.
- **Built-in itertools.permutations**: `O(n! × n)` - for storing the result; the generator uses `O(n)` internal state.

### Trade-offs

- **Backtracking with Path Building**: Clearest to narrate and extends to duplicates, at the cost of an `O(n)` membership scan per choice.
- **Backtracking with Used Array**: Removes the membership scan with an `O(1)` lookup, adding one small auxiliary array.
- **Backtracking with Index Swapping**: The most space-frugal variant, but it mutates the input and is the least intuitive to read.
- **Iterative Build-Up**: Recursion-free and easy to reason about, but it holds every intermediate generation in memory.
- **Heap's Algorithm**: Minimal-change generation with a single swap between consecutive permutations, but the parity rule is opaque, it mutates the input, and the emission order is unintuitive.
- **Built-in itertools.permutations**: Concise and fast, but hides the algorithm and is unsuitable for interviews.

### When to Use Each

- **Backtracking with Path Building** (recommended): Best for interviews and learning. The choose, explore, unchoose template is the clearest to explain.
- **Backtracking with Used Array**: When you want the same clarity with a better constant factor, or anticipate generalizing to duplicate values.
- **Backtracking with Index Swapping**: When space is at a premium and mutating the input array is acceptable.
- **Iterative Build-Up**: When a non-recursive construction is preferred and the extra intermediate memory is acceptable.
- **Heap's Algorithm**: When consecutive permutations should differ minimally, such as incrementally re-evaluating a function of the arrangement after each swap; it is a CS classic rather than an expected interview answer.
- **Built-in itertools.permutations**: For production code where performance and conciseness matter more than demonstrating algorithmic knowledge.

### Optimization Notes

- Since every approach shares the `O(n! × n)` time floor, optimization here is about space and clarity rather than asymptotic speed.
- The path-building membership scan is the one avoidable cost: swapping it for an indexed `used` array turns an `O(n)` check into `O(1)`.
- When mutating the input is acceptable, the index-swapping approach removes the per-call `path` allocation entirely.
- Heap's algorithm pushes generation cost to its floor, one swap per permutation, but the mandatory `O(n)` copy per output means the overall `O(n! × n)` bound does not budge.
- A key pitfall across the backtracking variants is appending the live working list instead of a copy; always append `path[:]` or `current[:]` so later mutations do not corrupt stored results.
