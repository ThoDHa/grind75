# [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/)

Easy - 10 minutes - Array, Hash Table, Sorting

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

### Solution 1: Dictionary/Counter Approach

```python
def containsDuplicate(self, nums: List[int]) -> bool:
    counter = {}
    
    for num in nums:
        if counter.get(num, 0) != 0:
            return True
        counter[num] = 1
    return False
```

#### Approach

This approach uses a dictionary to keep track of numbers we've seen. For each number, we check if it already exists in our dictionary. If it does, we've found a duplicate and return `True`. Otherwise, we add the number to the dictionary and continue. If we process all numbers without finding a duplicate, we return `False`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We traverse the array once, and dictionary operations (lookups and insertions) are `O(1)` on average.

##### Space Complexity: `O(n)`

In worst case, we might need to store all elements in the dictionary if there are no duplicates.

#### Key Insights

- Uses a hash map to track seen elements
- Early return when a duplicate is found
- Simple implementation with good performance

### Solution 2: Set Approach

```python
def containsDuplicate(self, nums: List[int]) -> bool:
    return len(set(nums)) < len(nums)
```

#### Approach

This elegant solution uses Python's built-in `set` data structure, which only keeps unique elements. We create a set from the input array and compare its length with the original array. If the set has fewer elements than the original array, it means there were duplicates.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Creating a set requires traversing the entire array once.

##### Space Complexity: `O(n)`

In worst case, we store all unique elements in the set.

#### Key Insights

- Concise, Pythonic solution leveraging built-in data structures
- Takes advantage of set's property of only containing unique elements
- More readable but functionally equivalent to iterative approach

### Solution 3: Sorting Approach

```python
def containsDuplicate(self, nums: List[int]) -> bool:
    nums.sort()
    for i in range(1, len(nums)):
        if nums[i] == nums[i-1]:
            return True
    return False
```

#### Approach

This solution first sorts the array, bringing identical elements adjacent to each other. Then it scans through the sorted array, checking if any adjacent elements are identical.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting the array takes `O(n log n)` time, and the subsequent scan takes `O(n)` time.

##### Space Complexity: `O(1)` or `O(n)`

The space complexity depends on the sorting algorithm implementation. Some sorting algorithms use `O(1)` extra space, while others might use `O(n)`.

#### Key Insights

- Simplifies the problem by first ordering the elements
- Does not require additional data structures (in some implementations)
- Less efficient than hash-based approaches due to sorting cost

## Comparison of Solutions

### Time Complexity

- **Dictionary Approach**: `O(n)` - Single pass with constant-time lookups
- **Set Approach**: `O(n)` - Creating a set requires iterating through all elements once
- **Sorting Approach**: `O(n log n)` - Limited by sorting algorithm efficiency

### Space Complexity

- **Dictionary Approach**: `O(n)` - Stores at most n items in the dictionary
- **Set Approach**: `O(n)` - Stores unique elements in the set
- **Sorting Approach**: `O(1)` to `O(n)` - Depends on sorting implementation

### Trade-offs

- Dictionary and set approaches have optimal time complexity but require additional memory
- Sorting approach may use less memory but is slower due to the `O(n log n)` sorting step
- Set approach offers the most concise solution but requires understanding of set properties

### When to Use Each

- **Dictionary Approach**: Good for explicit tracking and when early return is beneficial
- **Set Approach**: Best for simple, concise code when performance is important
- **Sorting Approach**: Useful when memory constraints are strict and time is less critical

### Optimization Notes

- The dictionary approach allows early termination upon finding the first duplicate
- The set approach is most concise but processes all elements regardless
- The sorting approach could be memory-efficient but is generally slower

```
