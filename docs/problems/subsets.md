# [Subsets](https://leetcode.com/problems/subsets/)

**Medium** | **30 minutes** | **Array, Backtracking, Bit Manipulation**

**Pattern:** [Backtracking](../patterns/backtracking_exploration/intuition.md)

**Practice:** [`practice/subsets/solution.py`](../../practice/subsets/solution.py)

Given an integer array `nums` of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.

## Examples

### Example 1

**Input:** `nums = [1,2,3]`

**Output:** `[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]`

### Example 2

**Input:** `nums = [0]`

**Output:** `[[],[0]]`

## Constraints

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`
- All the numbers of `nums` are unique.

## Solutions

### Iterative Build-Up

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        # Start with empty subset
        result = [[]]

        # For each number in input
        for num in nums:
            # Create new subsets by adding current number to all existing subsets
            new_subsets = []
            for existing_subset in result:
                # Create new subset with current number added
                new_subset = existing_subset + [num]
                new_subsets.append(new_subset)

            # Add all new subsets to result
            result.extend(new_subsets)

        return result
```

#### Approach

This iterative approach builds the power set incrementally. We start with just the empty subset, then for each new element, we duplicate all existing subsets and add the new element to the duplicates.

The progression for nums = [1,2,3]:
- Start: [[]]
- Add 1: [[], [1]]
- Add 2: [[], [1], [2], [1,2]]
- Add 3: [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]

This demonstrates how the power set can be constructed systematically without recursion.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n)`

For each element (n iterations), we process all existing subsets (up to 2^(i-1) subsets in iteration i) and create new subsets taking O(n) time each.

##### Space Complexity: `O(2^n × n)`

We store all intermediate and final subsets. The result list grows from 1 to 2^n subsets.

#### Key Insights

- Each new element doubles the number of subsets, which is why the result grows from 1 to `2^n` entries.
- Building `existing_subset + [num]` creates a fresh list, so no two result entries alias the same object.
- The approach needs no recursion and no index bookkeeping, making it the easiest to reason about step by step.

### Backtracking

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []

        def backtrack(start_index, current_subset):
            # Add current subset to result (creates a copy)
            result.append(current_subset[:])

            # Try adding each remaining element to current subset
            for i in range(start_index, len(nums)):
                # Choose: add nums[i] to current subset
                current_subset.append(nums[i])

                # Explore: recursively build subsets that include nums[i]
                backtrack(i + 1, current_subset)

                # Unchoose: remove nums[i] for next iteration (backtrack)
                current_subset.pop()

        backtrack(0, [])
        return result
```

#### Approach

This backtracking solution uses the classic "choose, explore, unchoose" pattern. For each element, we make a binary decision: include it in the current subset or skip it. The `start_index` parameter ensures we don't revisit earlier elements, preventing duplicate subsets.

The key insight is that we add the current subset to results at every recursive call (not just base cases), since every partial subset is a valid subset. This naturally generates all 2^n possible subsets.

Unlike permutations where we build complete arrangements, here every intermediate state represents a valid subset.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n)`

There are 2^n subsets to generate, and each subset takes O(n) time to copy into the result array.

##### Space Complexity: `O(2^n × n + n)`

O(2^n × n) for storing all subsets in the result, plus O(n) for the recursion stack depth and current subset tracking.

#### Key Insights

- The `start_index` parameter enforces a canonical element order, which is what prevents `[1, 2]` and `[2, 1]` from both appearing.
- Recording `current_subset[:]` at every node (not just leaves) captures all `2^n` subsets, since every partial path is itself a valid subset.
- Appending a copy is essential; appending `current_subset` directly would leave every result entry pointing at the same list that later gets mutated.

### Recursive Choose or Skip

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        def generate_subsets(index, current_subset):
            # Base case: processed all elements
            if index == len(nums):
                return [current_subset[:]]  # Return copy of current subset

            # Recursive case: choose or skip current element
            result = []

            # Skip current element: don't include nums[index]
            result.extend(generate_subsets(index + 1, current_subset))

            # Choose current element: include nums[index]
            current_subset.append(nums[index])
            result.extend(generate_subsets(index + 1, current_subset))
            current_subset.pop()  # Backtrack

            return result

        return generate_subsets(0, [])
```

#### Approach

This recursive solution makes the binary choice explicit: for each element, we recursively explore both possibilities (include it or skip it). This creates a binary decision tree where each path from root to leaf represents a unique subset.

The approach differs from the Iterative Build-Up by making the choice or skip decision explicit and only adding complete subsets at base cases, rather than adding partial subsets during recursion.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n)`

We explore 2^n paths in the decision tree, each requiring O(n) time to copy the subset.

##### Space Complexity: `O(2^n × n + n)`

O(2^n × n) for storing results, plus O(n) for recursion stack depth and current subset tracking.

#### Key Insights

- Each element contributes exactly one binary branch (skip then choose), so the recursion tree has `2^n` leaves, one per subset.
- Subsets are collected only at the base case, which keeps the recursion structurally symmetric with the permutation template.
- The skip branch runs before the choose branch, but ordering of the two branches only affects output order, not correctness.

### Bit Manipulation

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        result = []

        # Iterate through all possible bitmasks from 0 to 2^n - 1
        for mask in range(1 << n):  # 1 << n is 2^n
            subset = []

            # Check each bit position in the current mask
            for i in range(n):
                # If bit i is set in mask, include nums[i] in subset
                if mask & (1 << i):
                    subset.append(nums[i])

            result.append(subset)

        return result
```

#### Approach

This elegant approach uses bit manipulation to represent all possible subset combinations. Each number from 0 to 2^n - 1 represents a unique subset when interpreted as a bitmask:
- Bit 0 represents whether nums[0] is included
- Bit 1 represents whether nums[1] is included
- And so on...

For example, with nums = [1,2,3]:
- 000 (0) → []
- 001 (1) → [1]
- 010 (2) → [2]
- 011 (3) → [1,2]
- 100 (4) → [3]
- etc.

This provides a direct mathematical mapping between integers and subsets.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n)`

We iterate through 2^n bitmasks, and for each mask, we check n bits and potentially add n elements.

##### Space Complexity: `O(2^n × n)`

For storing all subsets in the result array. The algorithm itself uses O(1) extra space.

#### Key Insights

- The integers `0` to `2^n - 1` enumerate every subset exactly once, with bit `i` deciding whether `nums[i]` is included.
- No recursion stack is needed, so the only extra space beyond the output is a single integer mask.
- This mapping is clean only while `n` is small enough to fit in one machine integer, which the constraint `n ≤ 10` guarantees.

## Comparison of Solutions

### Time Complexity

- **Iterative Build-Up**: `O(2^n × n)` - For each of n elements we process all existing subsets, creating new ones in O(n).
- **Backtracking**: `O(2^n × n)` - There are 2^n subsets to generate, and copying each into the result takes O(n).
- **Recursive Choose or Skip**: `O(2^n × n)` - We explore 2^n paths in the decision tree, each requiring O(n) to copy the subset.
- **Bit Manipulation**: `O(2^n × n)` - We iterate through 2^n bitmasks, checking n bits per mask.

### Space Complexity

- **Iterative Build-Up**: `O(2^n × n)` - Stores all intermediate and final subsets, with higher intermediate space usage.
- **Backtracking**: `O(2^n × n + n)` - O(2^n × n) to store all subsets, plus O(n) for the recursion stack and current subset.
- **Recursive Choose or Skip**: `O(2^n × n + n)` - O(2^n × n) for results, plus O(n) for recursion stack and current subset.
- **Bit Manipulation**: `O(2^n × n)` - For storing all subsets; the algorithm itself uses O(1) extra space.

### Trade-offs

- **Iterative Build-Up**: Non-recursive and easy to follow step-by-step, but uses more intermediate space as subsets are duplicated.
- **Backtracking**: Clear logic that is educational and easily extensible to handle duplicates or constraints, at the cost of recursion overhead.
- **Recursive Choose or Skip**: Makes the binary include or skip choice explicit, but has a more complex recursion structure.
- **Bit Manipulation**: Elegant with a direct integer-to-subset mapping and no recursion, but less intuitive and harder to extend.

### When to Use Each

- **Iterative Build-Up**: For those who prefer iterative solutions or need to understand incremental construction.
- **Backtracking (Recommended)**: Best for interviews: clear, extensible to handle duplicates or constraints.
- **Recursive Choose or Skip**: For educational purposes to understand the binary decision tree structure.
- **Bit Manipulation**: When you want to demonstrate mathematical insight or avoid recursion.

### Optimization Notes

- All four solutions share the same `O(2^n × n)` time complexity because the power set inherently contains 2^n subsets, so none is asymptotically faster than another.
- Backtracking is the recommended approach for interviews: it reads clearly and extends naturally to variations such as subsets with duplicates (sort then skip equal elements) or fixed-size k-combinations.
- Bit manipulation avoids recursion entirely and offers the lowest constant overhead, but only works cleanly when n is small enough for a single integer mask (here n ≤ 10).
- A common pitfall in backtracking is appending `current_subset` directly instead of a copy (`current_subset[:]`); without the copy, all result entries reference the same mutated list.
