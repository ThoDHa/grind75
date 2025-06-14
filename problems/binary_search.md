# [Binary Search](https://leetcode.com/problems/binary-search/)

Easy - 15 minutes - Binary Search

Given an array of integers `nums` which is sorted in ascending order, and an
integer `target`, write a function to search `target` in `nums`. If `target`
exists, then return its index. Otherwise, return -1.

You must write an algorithm with `O(log n)` runtime complexity.

## Examples

### Example 1

**Input:** `nums = [-1,0,3,5,9,12]`, `target = 9`

**Output:** `4`

**Explanation:** `9` exists in `nums` and its index is `4`.

### Example 2

**Input:** `nums = [-1,0,3,5,9,12]`, `target = 2`

**Output:** `-1`

**Explanation:** `2` does not exist in `nums` so return `-1`.

## Constraints

- `1 <= nums.length <= 10^4`
- `-10^4 < nums[i], target < 10^4`
- All the integers in `nums` are unique.
- `nums` is sorted in ascending order.

## Solutions

### Solution 1: Recursive Binary Search

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        return self._binary_search(nums, 0, len(nums)-1, target)
        
    def _binary_search(self, nums: List[int], start: int, stop: int, target) -> int:
        if (start > stop):
            return -1
        middle = start + ((stop - start)//2)
        middle_value = nums[middle]
        if (middle_value == target):
            return middle
        if (middle_value < target):
            return self._binary_search(nums, middle+1, stop, target)
        else:
            return self._binary_search(nums, start, middle-1, target)
```

### Approach

This solution implements a classic recursive binary search algorithm to find a target value in a sorted array:

1. We define a helper function `_binary_search` that takes the array, search range boundaries, and target
2. Base case: If start > stop (invalid range), return -1 indicating target not found
3. Calculate the middle index using `start + ((stop - start)//2)` to avoid potential integer overflow
4. If the middle element equals the target, return its index
5. If the middle element is smaller than target, search the right half (middle+1 to stop)
6. If the middle element is larger than target, search the left half (start to middle-1)

### Time and Space Complexity Analysis

#### Time Complexity: `O(log n)`

- Each recursive call divides the search space in half
- For an array of size n, we make at most log₂(n) recursive calls
- This meets the problem's requirement for logarithmic runtime complexity

#### Space Complexity: `O(log n)`

- The space complexity is determined by the recursion call stack depth
- For binary search, this is logarithmic in the input size

### Key Insights

- The solution uses the "divide and conquer" paradigm to efficiently search the array
- The calculation of the middle index as `start + ((stop - start)//2)` prevents integer overflow
- The recursive approach provides a clean and intuitive implementation of binary search

### Solution 2: Iterative Binary Search

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        
        while left <= right:
            mid = left + (right - left) // 2
            
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
                
        return -1
```

### Approach

This solution takes an iterative approach to binary search, eliminating the need for recursion:

1. Initialize two pointers, `start` and `stop`, to the start and end of the array
2. While the search range is valid (left ≤ right):
   - Calculate the middle index to avoid overflow
   - If the middle element equals the target, return its index
   - If the middle element is less than the target, search the right half
   - If the middle element is greater than the target, search the left half
3. If the loop exits, return -1 indicating target not found

### Time and Space Complexity Analysis

#### Time Complexity: `O(log n)`

- Each iteration halves the search space
- For an array of size n, we need at most log₂(n) iterations
- This maintains the logarithmic runtime requirement

#### Space Complexity: `O(1)`

- The solution uses a constant amount of extra space regardless of input size
- No recursive call stack is needed

### Key Insights

- The iterative approach achieves the same functionality as the recursive solution
- Eliminating recursion improves space efficiency
- This approach is often preferred in practice due to its constant space complexity

## Comparison of Solutions

### Time Complexity

- **Solution 1 (Recursive)**: `O(log n)` - Logarithmic time due to halving the search space
- **Solution 2 (Iterative)**: `O(log n)` - Same logarithmic time complexity

### Space Complexity

- **Solution 1 (Recursive)**: `O(log n)` - Space for the recursion call stack
- **Solution 2 (Iterative)**: `O(1)` - Constant space regardless of input size

### Trade-offs

- **Solution 1** offers a clean, intuitive implementation that closely mirrors the binary search concept
- **Solution 2** provides better space efficiency by avoiding the recursion stack

### When to Use Each

- **Solution 1 (Recursive)**: When code readability is prioritized and the input size is moderate
- **Solution 2 (Iterative)**: When space efficiency is important or when dealing with large inputs

### Optimization Notes

- Both solutions calculate the middle index as `start + (stop - start) // 2` to prevent potential integer overflow
- For very deep recursion (extremely large arrays), the iterative solution would prevent stack overflow errors
- The iterative approach is generally preferred in production code for its space efficiency
