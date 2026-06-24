# [Majority Element](https://leetcode.com/problems/majority-element/)

**Easy** | **15 minutes** | **Array, Hash Table, Divide and Conquer**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Practice:** [`practice/majority_element/solution.py`](../../practice/majority_element/solution.py)

Given an array `nums` of size `n`, return the majority element.

The majority element is the element that appears more than `⌊n / 2⌋` times. You may assume that the majority element always exists in the array.

## Examples

### Example 1

**Input:** `nums = [3,2,3]`

**Output:** `3`

### Example 2

**Input:** `nums = [2,2,1,1,1,2,2]`

**Output:** `2`

## Constraints

- `n == nums.length`
- `1 <= n <= 5 * 10^4`
- `-10^9 <= nums[i] <= 10^9`
- The majority element always exists in the array.

## Follow-up

- Could you solve the problem in linear time and in `O(1)` space?

## Solutions

### Brute Force

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        n = len(nums)
        for candidate in nums:
            count = 0
            for num in nums:
                if num == candidate:
                    count += 1
            if count > n // 2:
                return candidate
        return nums[0]
```

#### Approach

The most direct idea follows straight from the definition: the majority element
is the one appearing more than `⌊n / 2⌋` times, so try each value and count its
occurrences by hand. The steps:

1. For each candidate value in the array, scan the whole array and tally how many
   times that value appears.
2. As soon as a candidate's tally exceeds `n // 2`, return it.
3. The trailing `return nums[0]` only satisfies the type signature; the guarantee
   that a majority exists means one candidate always wins first.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

For each of the `n` candidates, an inner pass scans all `n` elements to count
matches, giving `n * n` work in the worst case.

##### Space Complexity: `O(1)`

Only the scalar `count` and `n` are tracked; no structure grows with the input.

#### Key Insights

- Transcribes the problem definition literally: count each value, return the one
  over half.
- Requires no extra data structures, but pays a quadratic price for it.
- A natural starting point that every later approach exists to speed up.

### Hash Map

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        counts = {}
        for num in nums:
            counts[num] = counts.get(num, 0) + 1

        majority = nums[0]
        for num, count in counts.items():
            if count > counts[majority]:
                majority = num
        return majority
```

#### Approach

Count how many times each value appears, then return whichever value carries the
highest count. The steps:

1. Walk the array once, incrementing a per-value counter in a dictionary.
2. Walk the dictionary once, tracking the value whose count is largest.
3. Return that value.

Because the majority element appears more than `⌊n / 2⌋` times, its count strictly
exceeds every other count, so the maximum-count value is guaranteed to be the
answer.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The first pass over the array is `O(n)`. The dictionary holds at most `n` distinct
keys, so the second pass is also `O(n)`. The total is `O(n)`.

##### Space Complexity: `O(n)`

In the worst case (all values distinct except for the majority), the dictionary
stores up to `n` key-value pairs.

#### Key Insights

- Intuitive and directly self-derivable: count, then take the most frequent value.
- Works even without the majority guarantee, in which case it returns the mode.
- Trades extra space for simplicity and a single linear scan of counting.

### Boyer-Moore Voting Algorithm

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        count = 0
        candidate = None

        for num in nums:
            if count == 0:
                candidate = num
            count += 1 if num == candidate else -1

        return candidate
```

#### Approach

Maintain a single `candidate` and a running `count`. The steps:

1. When `count` is zero, adopt the current value as the new `candidate`.
2. Increment `count` when the current value matches the candidate, decrement it
   otherwise.
3. After the pass, the surviving `candidate` is the majority element.

Conceptually, each non-majority value cancels out one majority value. Since the
majority element appears more than `⌊n / 2⌋` times, it cannot be fully cancelled
and remains as the final candidate.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

A single pass over the array.

##### Space Complexity: `O(1)`

Only two scalar variables are used, regardless of input size.

#### Key Insights

- Satisfies the follow-up: linear time and constant space.
- The pairwise-cancellation argument depends on the strict "more than half" count.
- No sorting and no auxiliary structure, making it ideal for large inputs.

### Sorting

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        nums.sort()
        return nums[len(nums) // 2]
```

#### Approach

Sort the array and return the middle element. Any value occupying more than half
the positions must straddle the center index after sorting, so the element at
index `len(nums) // 2` is always the majority element.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Dominated by the sort. The single index lookup afterward is `O(1)`.

##### Space Complexity: `O(1)` or `O(n)`

An in-place sort uses `O(1)` auxiliary space; sorts that allocate a copy use
`O(n)`. Python's `list.sort` uses `O(n)` in the worst case.

#### Key Insights

- Extremely concise once the center-index observation is made.
- Correctness rests entirely on the "more than half" guarantee filling the middle.
- Slower than linear approaches because of the sort, and it mutates the input.

### Counter

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        return Counter(nums).most_common(1)[0][0]
```

#### Approach

Let the standard library do the counting. `Counter(nums)` tallies frequencies in
one pass, and `most_common(1)` returns the single highest-frequency `(value,
count)` pair, from which we take the value.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Building the `Counter` is `O(n)`. `most_common(1)` finds the single largest entry
in `O(n)` rather than sorting all entries.

##### Space Complexity: `O(n)`

The `Counter` stores up to `n` distinct keys, matching the hand-written hash map.

#### Key Insights

- The most concise correct solution, delegating the core work to `collections`.
- Functionally equivalent to the Hash Map approach with the same complexity.
- Requires `from collections import Counter`; prefer it only when a one-liner is acceptable.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - for each candidate, a full inner pass counts matches.
- **Hash Map**: `O(n)` - two linear passes, counting then selecting the maximum.
- **Boyer-Moore Voting Algorithm**: `O(n)` - a single linear pass.
- **Sorting**: `O(n log n)` - dominated by the sort.
- **Counter**: `O(n)` - one pass to tally, one selection of the largest entry.

### Space Complexity

- **Brute Force**: `O(1)` - only a running count and the length are tracked.
- **Hash Map**: `O(n)` - dictionary of per-value counts.
- **Boyer-Moore Voting Algorithm**: `O(1)` - two scalar variables.
- **Sorting**: `O(1)` in place, otherwise `O(n)`.
- **Counter**: `O(n)` - `Counter` of per-value counts.

### Trade-offs

- The Brute Force approach needs no extra space and reads straight off the definition, but its quadratic time is too slow at the upper constraint.
- The Hash Map approach is intuitive and works without the majority guarantee, but spends `O(n)` extra space.
- The Boyer-Moore approach is the most efficient on both axes, at the cost of a less obvious correctness argument.
- The Sorting approach is short but pays an `O(n log n)` cost and mutates the input.
- The Counter approach matches the Hash Map's behavior in a single line, trading explicitness for brevity.

### When to Use Each

- **Brute Force**: Only as a first sketch or for tiny inputs where clarity beats speed.
- **Hash Map**: When readability matters or the majority guarantee may not hold.
- **Boyer-Moore Voting Algorithm**: When optimal time and space are required, especially for large inputs (Recommended for the follow-up).
- **Sorting**: When implementation simplicity outweighs performance.
- **Counter**: When a concise, idiomatic one-liner is acceptable and `O(n)` space is fine.

### Optimization Notes

- Boyer-Moore is the only approach that meets the follow-up's `O(1)` space target; it leverages the strict "more than `⌊n / 2⌋`" guarantee so the candidate can never be fully cancelled.
- When the majority element is not guaranteed to exist, follow Boyer-Moore with a verification pass that counts the candidate's occurrences, or fall back to the Hash Map or Counter approach.
