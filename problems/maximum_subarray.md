# [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/)

Easy - 20 minutes - Array, Dynamic Programming, Divide and Conquer

Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return *its sum*.

A **subarray** is a contiguous part of an array.

## Examples

### Example 1

**Input:** `nums = [-2,1,-3,4,-1,2,1,-5,4]`

**Output:** `6`

**Explanation:** The subarray `[4,-1,2,1]` has the largest sum 6.

### Example 2

**Input:** `nums = [1]`

**Output:** `1`

**Explanation:** The subarray `[1]` has the largest sum 1.

### Example 3

**Input:** `nums = [5,4,-1,7,8]`

**Output:** `23`

**Explanation:** The subarray `[5,4,-1,7,8]` has the largest sum 23.

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

**Follow up:** If you have figured out the `O(n)` solution, try coding another solution using the **divide and conquer approach**, which is more subtle.

## Solutions

### Solution 1: Kadane's Algorithm

```python
def maxSubArray(self, nums: List[int]) -> int:
    max_current = max_global = nums[0]
    
    for i in range(1, len(nums)):
        # Either take the current element or add it to the previous subarray
        max_current = max(nums[i], max_current + nums[i])
        # Update the maximum sum found so far
        if max_current > max_global:
            max_global = max_current
            
    return max_global
```

#### Approach

Kadane's algorithm works by maintaining two variables: `max_current` (maximum sum ending at current position) and `max_global` (maximum sum found so far). For each element, we decide whether to start a new subarray or extend the existing one by comparing the current element with the sum of the current element and previous subarray.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The solution traverses the array exactly once.

##### Space Complexity: `O(1)`

Only a constant amount of extra space is used regardless of input size.

#### Key Insights

- Dynamic programming approach that builds the solution incrementally
- At each step, we make a local optimal choice (whether to start a new subarray or extend)
- Efficiently handles both positive and negative numbers

### Solution 2: Divide and Conquer

```python
def maxSubArray(self, nums: List[int]) -> int:
    def find_max_subarray(arr, left, right):
        # Base case: single element
        if left == right:
            return arr[left]
            
        # Find middle point
        mid = (left + right) // 2
            
        # Find maximum subarray sum that crosses the midpoint
        left_sum = float('-inf')
        current_sum = 0
        for i in range(mid, left - 1, -1):
            current_sum += arr[i]
            left_sum = max(left_sum, current_sum)
            
        right_sum = float('-inf')
        current_sum = 0
        for i in range(mid + 1, right + 1):
            current_sum += arr[i]
            right_sum = max(right_sum, current_sum)
            
        # Find maximum subarray sum in left and right halves
        left_max = find_max_subarray(arr, left, mid)
        right_max = find_max_subarray(arr, mid + 1, right)
            
        # Return maximum of the three
        return max(left_max, right_max, left_sum + right_sum)
        
    return find_max_subarray(nums, 0, len(nums) - 1)
```

#### Approach

This approach divides the array into halves recursively and finds the maximum subarray sum in three cases:

1. The maximum subarray is entirely in the left half
2. The maximum subarray is entirely in the right half
3. The maximum subarray crosses the middle point

The algorithm computes these three values and returns the maximum.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Each level of recursion requires O(n) work, and there are O(log n) levels in the recursion tree.

##### Space Complexity: `O(log n)`

The recursion stack requires O(log n) space due to the depth of recursive calls.

#### Key Insights

- Demonstrates the divide-and-conquer paradigm
- More complex than Kadane's but conceptually elegant
- Handles the "crossing the middle" case explicitly

## Comparison of Solutions

### Time Complexity

- **Kadane's Algorithm**: `O(n)` - Single linear scan through the array
- **Divide and Conquer**: `O(n log n)` - Each recursive level requires O(n) work

### Space Complexity

- **Kadane's Algorithm**: `O(1)` - Uses only a constant amount of extra space
- **Divide and Conquer**: `O(log n)` - Requires stack space for recursive calls

### Trade-offs

- Kadane's algorithm is more efficient both in time and space complexity
- Divide and conquer approach is more complex but demonstrates an important algorithmic paradigm
- Kadane's is iterative while divide and conquer is recursive

### When to Use Each

- **Kadane's Algorithm**: Preferred for most practical applications due to its efficiency and simplicity
- **Divide and Conquer**: Useful for educational purposes or when other divide-and-conquer optimizations might be applicable

### Optimization Notes

- Kadane's algorithm can be simplified to a single-variable version in languages that provide built-in max functions
- The divide and conquer approach could potentially be parallelized for very large arrays
- Both approaches handle edge cases like all negative numbers, but Kadane's does it more elegantly
