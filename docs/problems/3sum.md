# [3Sum](https://leetcode.com/problems/3sum/)

**Medium** | **25 minutes** | **Array, Two Pointers, Sorting**

**Pattern:** [Two Pointers](../patterns/two_pointers/intuition.md)

**Practice:** [`practice/3sum/solution.py`](../../practice/3sum/solution.py)

Given an integer array nums, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

Notice that the solution set must not contain duplicate triplets.

## Examples

### Example 1

**Input:** `nums = [-1,0,1,2,-1,-4]`

**Output:** `[[-1,-1,2],[-1,0,1]]`

**Explanation:**

- nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
- nums[0] + nums[2] + nums[4] = (-1) + 1 + (-1) = -1 + 0 = 0.
- nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2]. Notice that the order of the output and the order of the triplets does not matter.

### Example 2

**Input:** `nums = [0,1,1]`

**Output:** `[]`

**Explanation:** The only possible triplet does not sum up to 0.

### Example 3

**Input:** `nums = [0,0,0]`

**Output:** `[[0,0,0]]`

**Explanation:** The only possible triplet sums up to 0.

## Constraints

- `3 <= nums.length <= 3000`
- `-10^5 <= nums[i] <= 10^5`

## Solutions

### Brute Force

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        seen = set()
        result = []

        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        # Canonicalize the triplet so duplicates collapse:
                        # order the three values, then key on the tuple
                        a, b, c = nums[i], nums[j], nums[k]
                        if a > b:
                            a, b = b, a
                        if b > c:
                            b, c = c, b
                        if a > b:
                            a, b = b, a
                        triplet = (a, b, c)
                        if triplet not in seen:
                            seen.add(triplet)
                            result.append([a, b, c])

        return result
```

#### Approach

The most direct idea is to try every possible triplet of indices and keep the ones that sum to zero. With three distinct indices `i < j < k`, three nested loops enumerate every combination exactly once. The only wrinkle is deduplication: the same three values can appear at different index combinations, so each found triplet is normalized to a canonical order and tracked in a `seen` set.

1. Loop `i` from the first index to `n - 3`, `j` from `i + 1`, and `k` from `j + 1`, covering every unordered triple of positions.
2. When `nums[i] + nums[j] + nums[k] == 0`, sort the three values by hand (a fixed three-element ordering using swaps) to produce a canonical tuple.
3. Use the `seen` set to record canonical tuples, appending a triplet to the result only the first time its canonical form is encountered.

This is correct because every zero-sum triplet of values is enumerated by some index combination, and the canonical-tuple set guarantees each distinct value-triplet is reported exactly once.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n³)`

The three nested loops examine every combination of three indices, which is `C(n, 3)` triplets, so the work grows cubically. Each triplet does constant work (a sum, a fixed three-element sort, and one set operation).

##### Space Complexity: `O(n²)`

The `seen` set can hold up to one entry per distinct zero-sum triplet, which is `O(n²)` in the worst case (each pair of earlier values can combine with at most one complement). The output array is not counted toward auxiliary space.

#### Key Insights

- **Exhaustive enumeration needs no sorting**: trying all triplets directly is the most self-evident approach and exposes the raw `O(n³)` cost the smarter methods improve on.
- **Deduplication is the real difficulty**: even brute force must collapse repeated value-triplets, here via a canonical tuple stored in a set.
- **The bound is unsustainable**: at the constraint `n = 3000`, roughly `4.5` billion triplets make this too slow for submission, motivating the sorted two-pointer refinement.

### Sorting and Two Pointers

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []
        n = len(nums)

        for i in range(n - 2):
            # Skip duplicate values for the first number
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left, right = i + 1, n - 1

            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]

                if current_sum == 0:
                    result.append([nums[i], nums[left], nums[right]])

                    # Skip duplicates for the second number
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    # Skip duplicates for the third number
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1

                    left += 1
                    right -= 1

                elif current_sum < 0:
                    left += 1
                else:
                    right -= 1

        return result
```

#### Approach

The 3Sum problem is solved using a combination of sorting and the two-pointer technique. The key insight is to fix one number and then use two pointers to find pairs that sum to the negative of the fixed number.

Here's the step-by-step approach:

1. **Sort the array**: This enables us to use two pointers effectively and makes duplicate handling easier.

2. **Fix the first number**: Iterate through the array, using each element as the first number of our triplet. We only need to check up to `n-2` since we need at least two more elements.

3. **Two-pointer search**: For each fixed first number, use two pointers (`left` starting after the first number, `right` starting at the end) to find pairs that sum to `-nums[i]`.

4. **Handle duplicates carefully**: Skip duplicate values at all three positions to ensure unique triplets:
    - Skip duplicate first numbers in the main loop
    - Skip duplicate second and third numbers after finding a valid triplet

5. **Adjust pointers based on sum**:
    - If sum equals 0: found a triplet, record it and move both pointers
    - If sum is less than 0: increase sum by moving left pointer right
    - If sum is greater than 0: decrease sum by moving right pointer left

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

- Sorting takes O(n log n) time
- The outer loop runs O(n) times
- For each iteration of the outer loop, the two-pointer inner loop takes O(n) time in the worst case
- Overall: O(n log n) + O(n²) = O(n²)

##### Space Complexity: `O(1)` or `O(n)`

- If we don't count the output array, the space complexity is O(1) as we only use a constant amount of extra variables
- If we count the output array, the space complexity is O(n) in the worst case when there are many valid triplets
- The sorting operation may use O(log n) additional space depending on the implementation

#### Key Insights

- **Two-pointer technique**: After fixing one element, the problem reduces to finding two numbers that sum to a target (similar to Two Sum II on sorted array)
- **Duplicate handling is crucial**: The problem asks for unique triplets, so we must carefully skip duplicates at all three positions to avoid duplicate results
- **Sorted array enables optimization**: Sorting allows us to use two pointers and also makes it easy to skip duplicates by comparing adjacent elements
- **Early termination opportunity**: If the first number is positive, we can break early since all remaining numbers will also be positive (making sum impossible to be zero)

### Hash Set

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []
        n = len(nums)

        for i in range(n - 2):
            # Skip duplicate values for the first number
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # Track values already seen for the current fixed element
            seen = set()
            j = i + 1
            while j < n:
                # We need a third value that completes the triplet to zero
                complement = -(nums[i] + nums[j])
                if complement in seen:
                    result.append([nums[i], complement, nums[j]])
                    # Skip duplicate second numbers to keep triplets unique
                    while j + 1 < n and nums[j] == nums[j + 1]:
                        j += 1
                seen.add(nums[j])
                j += 1

        return result
```

#### Approach

This approach also fixes the first number but replaces the two-pointer scan with a hash set lookup. For each fixed element `nums[i]`, we walk the remainder of the array and, for every `nums[j]`, ask whether the complement `-(nums[i] + nums[j])` has already been seen. The array is sorted first so that both the fixed element and duplicate triplets can be skipped by comparing adjacent values.

Here's the step-by-step approach:

1. **Sort the array**: Sorting makes duplicate skipping straightforward because identical values become adjacent.

2. **Fix the first number**: Iterate through the array using each element as the first number, skipping any value equal to the previous one to avoid repeated triplets.

3. **Scan with a set**: For each fixed element, maintain a `seen` set of values encountered so far in the inner loop. Walking `j` from `i + 1` to the end, compute the complement `-(nums[i] + nums[j])`. If that complement is already in `seen`, the three values sum to zero.

4. **Skip duplicate triplets**: After recording a triplet, advance `j` past any consecutive equal values so the same triplet is not added twice. A `while` loop is used here (rather than a `for` loop) precisely so this manual advance of `j` persists.

5. **Record the current value**: Add `nums[j]` to `seen` before moving on, so future iterations can pair against it.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

- Sorting takes O(n log n) time
- The outer loop runs O(n) times
- For each fixed element, the inner scan visits up to O(n) elements with O(1) average set operations
- Overall: O(n log n) + O(n²) = O(n²)

##### Space Complexity: `O(n)`

- The `seen` set holds up to O(n) values for each fixed element
- This is more than the two-pointer approach, which uses only constant auxiliary space

#### Key Insights

- **Set replaces the inner two pointers**: Instead of converging two pointers, we trade O(1) auxiliary space for an O(n) hash set to find complements directly.
- **Sorting still earns its keep**: Although the set handles the lookup, sorting remains the cleanest way to skip duplicate first and second numbers.
- **Same asymptotic cost, different constants**: Both this and the two-pointer method are O(n²) in time, but the hash set adds linear space and incurs hashing overhead per element.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n³)` - Three nested loops enumerate every triplet of indices
- **Sorting and Two Pointers**: `O(n²)` - Sorting is O(n log n), then an O(n) outer loop each drives an O(n) two-pointer scan
- **Hash Set**: `O(n²)` - Sorting is O(n log n), then an O(n) outer loop each drives an O(n) set-based scan

### Space Complexity

- **Brute Force**: `O(n²)` - The `seen` set can hold up to one entry per distinct zero-sum triplet
- **Sorting and Two Pointers**: `O(1)` excluding the output - Uses only a constant number of pointer variables
- **Hash Set**: `O(n)` - Maintains a set of seen values for each fixed element

### Trade-offs

- The brute force is the most self-evident approach and needs no sorting, but its cubic time makes it unusable at the upper constraint and it still pays for deduplication
- The two-pointer approach uses constant auxiliary space and avoids hashing overhead, making it the leaner of the two quadratic methods
- The hash set approach is arguably easier to reason about for those already comfortable with the Two Sum hash pattern, at the cost of linear extra space
- Both quadratic methods rely on sorting to skip duplicates cleanly, so duplicate handling requires equal care in either version

### When to Use Each

- **Brute Force**: Only as a conceptual starting point or for tiny inputs; too slow to submit at `n = 3000`
- **Sorting and Two Pointers**: Preferred for interviews and production due to constant auxiliary space and predictable performance
- **Hash Set**: Useful when extending the familiar Two Sum hash technique to three numbers, or as a teaching bridge from Two Sum to 3Sum

### Optimization Notes

- The brute force can prune slightly by sorting and skipping repeated first values, but it remains cubic; the real speedup comes from replacing the innermost loop with a two-pointer or set scan
- The two-pointer version can break early once the fixed element becomes positive, since no triplet of sorted nonnegative values can sum to zero unless all are zero
- The hash set version reuses a fresh set per fixed element; clearing and reusing a single set can reduce allocations
- The two quadratic approaches share the same sorting step, so the dominant cost difference between them is the auxiliary space of the inner search
