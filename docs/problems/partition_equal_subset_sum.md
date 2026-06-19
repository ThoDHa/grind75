# [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/)

**Medium** | **30 minutes** | **Array, Dynamic Programming**

**Pattern:** [DP Knapsack/Subset](../patterns/dp_knapsack_subset/intuition.md)

**Practice:** [`practice/partition_equal_subset_sum/solution.py`](../../practice/partition_equal_subset_sum/solution.py)

Given an integer array `nums`, return `true` if you can partition the array into two subsets such that the sum of the elements in both subsets is equal.

## Examples

### Example 1

**Input:** `nums = [1,5,11,5]`

**Output:** `true`

**Explanation:** The array can be partitioned as `[1, 5, 5]` and `[11]`.

### Example 2

**Input:** `nums = [1,2,3,5]`

**Output:** `false`

**Explanation:** The array cannot be partitioned into equal sum subsets.

## Constraints

- `1 <= nums.length <= 200`
- `1 <= nums[i] <= 100`

## Solutions

### Bottom-Up DP

```python
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)

        # An odd total can never split into two equal halves.
        if total % 2 != 0:
            return False

        target = total // 2

        # dp[s] is True when some subset of the processed numbers sums to s.
        dp = [False] * (target + 1)
        dp[0] = True  # The empty subset sums to 0.

        for num in nums:
            # Walk downward so each number is used at most once (0/1 knapsack).
            for s in range(target, num - 1, -1):
                if dp[s - num]:
                    dp[s] = True

        return dp[target]
```

#### Approach

This is the textbook 0/1 subset-sum dynamic program. Two subsets have equal sum only
when the total is even and one subset sums to exactly `total // 2`, so an odd total
returns `False` immediately.

We then ask whether any subset sums to `target = total // 2`. Let `dp[s]` be `True`
when some subset of the numbers seen so far sums to `s`:

`dp[s] = dp[s] or dp[s - num]`

1. Initialize `dp` of size `target + 1` with `dp[0] = True` (the empty subset).
2. For each `num`, update `dp[s]` for `s` from `target` down to `num`. Iterating
   downward ensures `dp[s - num]` still refers to a state without the current `num`,
   enforcing the 0/1 (use-each-element-once) constraint.
3. Return `dp[target]`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × target)`

Each of the `n` numbers sweeps the `dp` array of size `target + 1`. Since
`target = total // 2`, this is `O(n × total)`: pseudo-polynomial in the sum.

##### Space Complexity: `O(target)`

A single boolean array of `target + 1` entries, reused across all numbers.

#### Key Insights

- The downward inner loop is what distinguishes 0/1 knapsack (each item once) from
  unbounded knapsack (an upward loop would let a number be reused).
- Rolling the classic 2D `dp[i][s]` table down to one row is safe precisely because
  the update only reads smaller indices of the previous state.
- The parity check is a free early exit that also guarantees `target` is an integer.

### Reachable Sum Set

```python
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)

        # An odd total can never split into two equal halves.
        if total % 2 != 0:
            return False

        target = total // 2

        # reachable holds every subset sum we can form so far.
        # Start with 0 (the empty subset).
        reachable = {0}

        for num in nums:
            next_reachable = set(reachable)
            for partial_sum in reachable:
                new_sum = partial_sum + num
                if new_sum == target:
                    return True
                if new_sum < target:
                    next_reachable.add(new_sum)
            reachable = next_reachable

        return target in reachable
```

#### Approach

This is a subset-sum problem in disguise. Two subsets have equal sum only when the
total is even and one subset sums to exactly `total // 2`. If the total is odd, no
partition can exist, so we return `False` immediately.

Once we have the target `total // 2`, the question becomes: can some subset of `nums`
sum to `target`? We answer it with a reachability set that tracks every subset sum
attainable with the elements processed so far:

1. Compute `total = sum(nums)`. If it is odd, return `False`.
2. Set `target = total // 2`.
3. Maintain a set `reachable` of achievable subset sums, seeded with `0`.
4. For each `num`, extend every existing reachable sum by `num`. If any reaches
   `target`, return `True`. Discard sums that exceed `target`, since they can never
   contribute to a valid partition.
5. After processing all numbers, return whether `target` was reached.

Capping reachable sums at `target` keeps the set bounded by `target + 1` distinct
values, which is what gives the algorithm its pseudo-polynomial bound.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × target)`

We process each of the `n` numbers once, and for each we iterate over the reachable
set, which holds at most `target + 1` distinct values. Since `target = total // 2`,
this is `O(n × total)` work overall: pseudo-polynomial in the sum of the elements.

##### Space Complexity: `O(target)`

The reachable set stores at most `target + 1` distinct subset sums.

#### Key Insights

- Equal partition is impossible unless the total is even, so the parity check is a
  free early exit that also guarantees `total // 2` is an integer.
- The problem reduces to a 0/1 subset-sum decision against the single target
  `total // 2`; each element is used at most once.
- Pruning sums above `target` bounds the state space and prevents wasted work.
- This reachable-set formulation is the dynamic programming recurrence in disguise:
  the Bottom-Up DP approach makes the same `dp[s]` explicit,
  while the Bitmask DP approach below packs it into a single integer.

### Bitmask DP

```python
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)

        # An odd total can never split into two equal halves.
        if total % 2 != 0:
            return False

        target = total // 2

        # Bit s of `bits` is set when some subset sums to s; only sum 0 starts set.
        bits = 1
        for num in nums:
            # Shifting left by num marks every (reachable sum + num) at once.
            bits |= bits << num

        # The answer is whether the target bit ended up set.
        return (bits >> target) & 1 == 1
```

#### Approach

This packs the entire boolean `dp` array into the bits of one Python integer, where
bit `s` plays the role of `dp[s]`. Python's arbitrary-precision integers make this a
clean, fast formulation:

1. Start with `bits = 1`, meaning only sum `0` is reachable (bit 0 set).
2. For each `num`, `bits << num` shifts every currently reachable sum up by `num`;
   OR-ing it back in (`bits |= bits << num`) records all the new reachable sums in a
   single machine-word-parallel operation.
3. After processing every number, test bit `target` with `(bits >> target) & 1`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × target / w)`

Each of the `n` shifts/ORs operates on a `target`-bit integer, which the interpreter
processes in machine words of width `w`. The asymptotic class matches the table DP,
but the per-bit constant factor is dramatically smaller.

##### Space Complexity: `O(target)`

A single integer holding `target + 1` significant bits.

#### Key Insights

- Bit `s` being set is exactly `dp[s]`; the shift-and-OR is the recurrence
  `dp[s] |= dp[s - num]` applied to all `s` simultaneously.
- Unlike the explicit downward loop, the bitset never risks reusing a number within
  one step because the shift reads the pre-update value of `bits`.
- This is the most concise and fastest approach in Python, but it leans on
  big-integer bit tricks and is less transparent than the table.

## Comparison of Solutions

### Time Complexity

- **Bottom-Up DP**: `O(n × target)` - sweep the boolean array per number.
- **Reachable Sum Set**: `O(n × target)` - iterate the bounded set per number.
- **Bitmask DP**: `O(n × target / w)` - same class with a small bitwise constant factor.

### Space Complexity

- **Bottom-Up DP**: `O(target)` - one boolean array.
- **Reachable Sum Set**: `O(target)` - at most `target + 1` distinct sums.
- **Bitmask DP**: `O(target)` - one integer of `target + 1` bits.

### Trade-offs

- The Bottom-Up DP approach is the clearest expression of the
  0/1 knapsack recurrence and the easiest to adapt to variants.
- The Reachable Sum Set approach reads naturally and prunes eagerly, but set objects
  carry more per-element overhead than a flat array.
- The Bitmask DP approach is the fastest and most compact, at the cost of relying on
  big-integer bit manipulation that is harder to read.

### When to Use Each

- **Bottom-Up DP**: The default choice for clarity and for
  explaining the knapsack structure.
- **Reachable Sum Set**: When a set-based formulation is more intuitive or when most
  sums stay sparse relative to `target`.
- **Bitmask DP**: When performance matters most in Python and the bitwise idiom is
  acceptable.

### Optimization Notes

- All three share the same pseudo-polynomial `O(n × target)` class; the differences
  are constant factors and readability.
- The downward inner loop in the table approach is the crucial detail that keeps the
  recurrence 0/1; an upward loop would silently solve the unbounded-knapsack variant.
- The bitmask formulation is typically the fastest in practice because CPython
  performs the shift and OR on wide machine words rather than per-element Python loops.
