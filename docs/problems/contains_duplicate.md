# [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/)

**Easy** | **10 minutes** | **Array, Hash Table, Sorting**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Practice:** [`practice/contains_duplicate/solution.py`](../../practice/contains_duplicate/solution.py)

Given an integer array `nums`, return `true` if any value appears **at least twice** in the array, and return `false` if every element is distinct.

## Examples

### Example 1

**Input:** `nums = [1,2,3,1]`

**Output:** `true`

**Explanation:** The value `1` appears twice in the array.

### Example 2

**Input:** `nums = [1,2,3,4]`

**Output:** `false`

**Explanation:** All elements in the array are distinct.

### Example 3

**Input:** `nums = [1,1,1,3,3,4,3,2,4,2]`

**Output:** `true`

**Explanation:** The array contains multiple duplicate values.

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

## Solutions

### Brute Force

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] == nums[j]:
                    return True
        return False
```

#### Approach

The most direct idea is to compare every pair of elements and report the first match:

1. For each index `i`, compare `nums[i]` against every later element `nums[j]` with `j > i`.
2. If any pair is equal, a duplicate exists, so return `True` immediately.
3. If no pair matches after checking all combinations, every element is distinct, so return `False`.

Pairing `i` with only the indices after it avoids comparing an element to itself and avoids checking the same pair twice. This requires no extra data structures: just two nested loops.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Every pair of indices is examined in the worst case, and there are roughly `n^2 / 2` such pairs, giving quadratic time.

##### Space Complexity: `O(1)`

Only a couple of loop counters are used; no storage grows with the input.

#### Key Insights

- The most self-evident approach: check every pair directly with no auxiliary structure.
- Constant extra space, but the quadratic time makes it too slow for the upper constraint of `10^5` elements.
- Starting `j` at `i + 1` avoids redundant and self comparisons.

### Hash Set

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False
```

#### Approach

Track every value as it is encountered and report the first repeat:

1. Initialize an empty set `seen`.
2. Iterate through `nums`. For each `num`, check whether it is already in `seen`.
3. If it is, a duplicate exists, so return `True` immediately.
4. Otherwise add `num` to `seen` and continue.
5. If the loop finishes without a hit, every element was distinct, so return `False`.

Membership tests and insertions on a hash set are constant time on average, which keeps the whole scan linear. The early return means the work stops the moment the first duplicate appears.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each element is processed once, and each set lookup and insertion is `O(1)` on average, giving `O(n)` total.

##### Space Complexity: `O(n)`

In the worst case (all distinct values), the set grows to hold every element.

#### Key Insights

- A hash set turns the "have I seen this before" question into an `O(1)` average operation.
- The early return avoids scanning the rest of the array once a duplicate is found.
- The logic is library-free: a plain `set` and a loop are all that is required.

### Sorting

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        nums = sorted(nums)
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                return True
        return False
```

#### Approach

Sorting brings equal values next to each other so duplicates can be spotted with a single adjacent-pair scan:

1. Sort a copy of `nums` into ascending order.
2. Walk from the second element to the last, comparing each element with its predecessor.
3. If any adjacent pair is equal, return `True`.
4. If no adjacent pair matches, return `False`.

This trades the extra hash-set memory for the cost of sorting. It is useful when auxiliary space is constrained and the input may be sorted in place.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The sort dominates at `O(n log n)`; the adjacent-pair scan adds only `O(n)`.

##### Space Complexity: `O(n)` or `O(1)`

Sorting a copy uses `O(n)` space; sorting the input in place keeps the extra space at `O(1)` aside from the sort's own overhead.

#### Key Insights

- Sorting collapses the duplicate search to a comparison of neighbors.
- No hash structure is needed, which can matter under tight memory budgets.
- It is slower than the hash approach because of the `O(n log n)` sort.

### Set Length Comparison

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return len(set(nums)) < len(nums)
```

#### Approach

A `set` discards duplicate values, so comparing sizes answers the question directly:

1. Build a set from `nums`, which keeps only distinct values.
2. If the set is smaller than the original list, at least one value was dropped as a duplicate, so return `True`.
3. Otherwise the sizes match and every element was unique, so return `False`.

The built-in `set` does the core deduplication work here, which is why this concise form is ranked after the hand-written approaches.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Building the set visits every element once.

##### Space Complexity: `O(n)`

The set stores all distinct values, up to `n` of them.

#### Key Insights

- Reduces the problem to a single length comparison.
- Reads cleanly but always processes the entire array, with no early exit.
- Relies on the language's `set` to perform the deduplication.

### Counter

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return any(count > 1 for count in Counter(nums).values())
```

#### Approach

`collections.Counter` tallies how many times each value appears, and any count above one signals a duplicate:

1. Build a `Counter` over `nums` to map each value to its frequency.
2. Scan the frequency values and return `True` as soon as one exceeds `1`.
3. If no count is greater than `1`, return `False`.

This leans most heavily on the standard library, so it sits last among the approaches.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Counting visits every element once, and scanning the distinct counts is at most `O(n)`.

##### Space Complexity: `O(n)`

The counter holds an entry for each distinct value.

#### Key Insights

- Produces full frequency information, which is more than this yes/no question needs.
- `any` short-circuits on the first count above one.
- Most library-driven of the options, so it ranks after the from-scratch solutions.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - compares every pair of elements.
- **Hash Set**: `O(n)` - single pass with constant-time average lookups.
- **Sorting**: `O(n log n)` - bounded by the sort step.
- **Set Length Comparison**: `O(n)` - one pass to build the set.
- **Counter**: `O(n)` - one pass to tally frequencies.

### Space Complexity

- **Brute Force**: `O(1)` - only loop counters, no auxiliary structure.
- **Hash Set**: `O(n)` - stores seen values, up to `n` of them.
- **Sorting**: `O(n)` or `O(1)` - depends on copying versus sorting in place.
- **Set Length Comparison**: `O(n)` - stores all distinct values.
- **Counter**: `O(n)` - stores a count per distinct value.

### Trade-offs

- The Brute Force approach needs no extra memory but its quadratic time is too slow at scale.
- The Hash Set approach is optimal in time and can exit early, at the cost of auxiliary memory.
- The Sorting approach avoids a hash structure but pays the `O(n log n)` sorting cost.
- The Set Length Comparison is the most concise but always scans the whole array.
- The Counter approach computes more information than needed but reads clearly.

### When to Use Each

- **Brute Force**: Only for tiny inputs or as a starting point before optimizing.
- **Hash Set**: The default choice when fastest detection with early exit matters.
- **Sorting**: When memory is tight and an in-place sort is acceptable.
- **Set Length Comparison**: When brevity and readability outweigh early termination.
- **Counter**: When frequencies are already needed elsewhere in the code.

### Optimization Notes

- The Brute Force approach uses no extra space but does redundant pairwise work; the Hash Set trades `O(n)` memory to cut the time to linear.
- The Hash Set approach terminates the moment the first duplicate is found, which is ideal when duplicates are common and appear early.
- The Sorting approach can drop to `O(1)` extra space by sorting the input in place when mutation is allowed.
- The Set Length Comparison and Counter forms favor clarity but process every element regardless of when a duplicate occurs.
