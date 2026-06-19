# [Two Sum](https://leetcode.com/problems/two-sum/)

**Easy** | **15 minutes** | **Array, Hash Table**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Practice:** [`practice/two_sum/solution.py`](../../practice/two_sum/solution.py)

Given an array of integers nums and an integer target, return indices of the two
numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not
use the same element twice.

You can return the answer in any order.

## Examples

### Example 1

**Input:** nums = `[2,7,11,15]`, target = `9`

**Output:** `[0,1]`

**Explanation:** Because `nums[0] + nums[1] == 9`, we return `[0, 1]`.

### Example 2

**Input:** nums = `[3,2,4]`, target = `6`

**Output:** `[1,2]`

### Example 3

**Input:** nums = `[3,3]`, target = `6`

**Output:** `[0,1]`

## Constraints

- `2 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
- Only one valid answer exists.

## Follow-up

Can you come up with an algorithm that is less than O(n²) time complexity?

## Solutions

### Brute-Force

```python
def twoSum(self, nums: List[int], target: int) -> List[int]:
    # Get the length of the input array
    length = len(nums)
    # Iterate through each element in the array
    for x in range(length):
        # Calculate the complement (value needed to reach target)
        complement = target - nums[x]
        # Check all elements after the current element
        for y in range(x+1, length):
            # If complement is found, return both indices
            if nums[y] == complement:
                return [x, y]
```

#### Approach

This brute force approach examines every possible pair of numbers in the array. For each element, it calculates the complement (`target - current number`) and checks all remaining elements to find this complement.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

The solution uses nested loops - for each of the `n` elements, we potentially check `n-1` other elements, resulting in `O(n²)` time complexity.

##### Space Complexity: `O(1)`

Only a constant amount of extra space is used regardless of input size.

#### Key Insights

- Simple and intuitive approach that works for all valid inputs
- Inefficient for large arrays due to quadratic time complexity
- No additional data structures required

### Sort and Two Pointers

```python
def twoSum(self, nums: List[int], target: int) -> List[int]:
    # Pair each value with its original index before sorting
    indexed = sorted(enumerate(nums), key=lambda pair: pair[1])
    left, right = 0, len(indexed) - 1
    while left < right:
        current_sum = indexed[left][1] + indexed[right][1]
        if current_sum == target:
            # Return the original indices, not the sorted positions
            return [indexed[left][0], indexed[right][0]]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []
```

#### Approach

This solution sorts the values and then converges two pointers from the ends of the sorted array. If the pointed values sum to less than the target, the left pointer moves right to increase the sum; if they sum to more, the right pointer moves left to decrease it. When the sum matches, we have found the pair.

Because the problem asks for the original indices, we cannot sort `nums` directly without losing that information. We instead pair each value with its original index before sorting, sort by value, and return the stored original indices when the matching pair is found.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting dominates the cost at `O(n log n)`, and the two-pointer scan that follows is a single `O(n)` pass.

##### Space Complexity: `O(n)`

Pairing each value with its original index produces a new list of `n` elements, requiring linear additional space.

#### Key Insights

- The two-pointer technique requires a sorted sequence, so sorting is a prerequisite rather than an optimization
- Tracking original indices is essential because the answer is expressed in terms of the unsorted input positions
- Faster than brute force yet slower than the hash map, this approach shines when a sorted order is needed anyway or when extra space for a hash map is undesirable

### Hash Map

```python
def twoSum(self, nums: List[int], target: int) -> List[int]:
    length = len(nums)
    nums_dict = {}
    for x in range(length):
        complement = target - nums[x]
        # Check if the complement exists in dictionary
        if complement in nums_dict:
            return [nums_dict[complement], x]
        # Store current number and its index
        nums_dict[nums[x]] = x
    return []
```

#### Approach

This solution uses a hash map to store previously encountered numbers and their indices. For each element, we check if its complement (`target - current number`) already exists in the hash map. If found, we've identified our pair. Otherwise, we add the current number and its index to the hash map.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We traverse the array only once, and hash map operations (lookups and insertions) are `O(1)` on average.

##### Space Complexity: `O(n)`

In worst case, we might need to store nearly all elements in the hash map before finding a solution.

#### Key Insights

- Trades space for time efficiency by using a hash map
- Single-pass algorithm with linear time complexity
- Demonstrates how auxiliary data structures can optimize solutions

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n²)` - Requires nested loops to check all possible pairs
- **Sort and Two Pointers**: `O(n log n)` - Sorting dominates, followed by a single linear two-pointer pass
- **Hash Map**: `O(n)` - Single-pass approach with constant-time lookups

### Space Complexity

- **Brute Force**: `O(1)` - Uses only a constant amount of extra space
- **Sort and Two Pointers**: `O(n)` - Stores value-index pairs to preserve original positions through sorting
- **Hash Map**: `O(n)` - Requires additional storage proportional to input size

### Trade-offs

- The brute force solution is simple to implement and uses minimal memory, but becomes impractically slow for large inputs
- The sort and two pointers solution beats brute force and avoids hashing, but the sort makes it slower than the hash map and the index bookkeeping adds complexity
- The hash map solution is significantly faster for large inputs but requires additional memory

### When to Use Each

- **Brute Force**: Suitable for very small inputs or memory-constrained environments where simplicity is valued over performance
- **Sort and Two Pointers**: Appropriate when the data is already sorted, when a sorted order is needed for other reasons, or when the two-pointer pattern is preferred
- **Hash Map**: Preferred for most practical applications, especially with larger datasets

### Optimization Notes

- The hash map approach demonstrates the classic space-time tradeoff in algorithm design
- By using a hash map to store previously seen values, we eliminate the need for the inner loop in the brute force approach
- The sort and two pointers approach removes the inner loop differently, by exploiting sorted order rather than a lookup table, but pays an `O(n log n)` sorting cost
- This is a common pattern in solving array problems: using additional data structures to achieve linear time complexity
