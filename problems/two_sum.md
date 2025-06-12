# [Two Sum](https://leetcode.com/problems/two-sum/)

Easy - 15 minutes - Array, Hash Table

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

### BruteForce

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

#### Solution Approach

This brute force approach examines every possible pair of numbers in the array. For each element, it calculates the complement (target - current number) and checks all remaining elements to find this complement.

#### Time and Space Complexity Analysis

##### Time Complexity: O(n²)

The solution uses nested loops - for each of the n elements, we potentially check n-1 other elements, resulting in O(n²) time complexity.

##### Space Complexity: O(1)

Only a constant amount of extra space is used regardless of input size.

#### Key Insights

- Simple and intuitive approach that works for all valid inputs
- Inefficient for large arrays due to quadratic time complexity
- No additional data structures required

### Hash Map

```python
def twoSum(self, nums: List[int], target: int) -> List[int]:
    length = len(nums)
    nums_dict = {}
    for x in range(length):
        complement = target - nums[x]
        # Check if the complement exists in dictionary
        if complement in nums_dict:
            return [x, nums_dict[complement]]
        # Store current number and its index
        nums_dict[nums[x]] = x
    return []
```

#### Solution Approach

This solution uses a hash map to store previously encountered numbers and their indices. For each element, we check if its complement (target - current number) already exists in the hash map. If found, we've identified our pair. Otherwise, we add the current number and its index to the hash map.

#### Time and Space Complexity Analysis

##### Time Complexity: O(n)

We traverse the array only once, and hash map operations (lookups and insertions) are O(1) on average.

##### Space Complexity: O(n)

In worst case, we might need to store nearly all elements in the hash map before finding a solution.

#### Key Insights

- Trades space for time efficiency by using a hash map
- Single-pass algorithm with linear time complexity
- Demonstrates how auxiliary data structures can optimize solutions
