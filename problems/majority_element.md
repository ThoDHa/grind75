# [Majority Element](https://leetcode.com/problems/majority-element/)

Easy - 15 minutes - Array, Hash Table, Divide and Conquer

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

### Solution 1: Hash Table

```python
def majorityElement(self, nums: List[int]) -> int:
    counter = {}

    for num in nums:
        counter[num] = counter.get(num, 0) + 1
    
    max = 0
    return_value = None
    for key, value in counter.items():
        if value > max:
            return_value, max = key, value
    return return_value
```

#### Solution 1: Approach

```

[file:problems/majority_element.md](problems/majority_element.md) line:54-71

```markdown
#### Solution 1: Approach

This solution uses a hash table (dictionary) to count the frequency of each element
in the array. We first iterate through the array to build a counter of each element.
Then, we find the element with the maximum count by iterating through the counter.

#### Solution 1: Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We traverse the array once to build the counter (`O(n)`) and then iterate through
the counter, which at most contains `n` distinct elements (`O(n)`). Therefore,
the total time complexity is `O(n)`.

##### Space Complexity: `O(n)`

In the worst case, if all elements are distinct, the counter would need to store
`n` key-value pairs.

#### Solution 1: Key Insights
```

[file:problems/majority_element.md](problems/majority_element.md) line:71-73

```markdown
#### Solution 1: Key Insights

- Simple and intuitive approach that works for all inputs
- Uses extra space to track frequency counts
- Requires two passes through the data (one for counting, one for finding maximum)
```

[file:problems/majority_element.md](problems/majority_element.md) line:73-86

```markdown
### Solution 2: Boyer-Moore Voting Algorithm

```python
def majorityElement(self, nums: List[int]) -> int:
    count = 0
    candidate = None
    
    for num in nums:
        if count == 0:
            candidate = num
        count += (1 if num == candidate else -1)
        
    return candidate
```

#### Solution 2: Approach

```

[file:problems/majority_element.md](problems/majority_element.md) line:88-106

```markdown
#### Solution 2: Approach

The Boyer-Moore Voting Algorithm is specifically designed for finding the majority
element. It works on the principle that if a majority element exists, it will
"survive" the pairwise cancellation of different elements. The algorithm maintains
a candidate element and a count. When the count reaches zero, we select a new
candidate.

#### Solution 2: Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We only need a single pass through the array.

##### Space Complexity: `O(1)`

We only use two variables (count and candidate) regardless of the input size.

#### Solution 2: Key Insights

- Satisfies the follow-up constraint of `O(1)` space complexity
- Works because the majority element appears more than `⌊n / 2⌋` times
- Elegant algorithm that doesn't require sorting or counting all elements
```

[file:problems/majority_element.md](problems/majority_element.md) line:108-116

```markdown
### Solution 3: Sorting

```python
def majorityElement(self, nums: List[int]) -> int:
    nums.sort()
    return nums[len(nums) // 2]
```

#### Solution 3: Approach

```

[file:problems/majority_element.md](problems/majority_element.md) line:116-134

```markdown
#### Solution 3: Approach

This solution sorts the array and returns the middle element. Since the majority
element appears more than `⌊n / 2⌋` times, it will always be at the middle position
after sorting.

#### Solution 3: Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Dominated by the sorting operation.

##### Space Complexity: `O(1)` or `O(n)`

If sorting in-place, the space complexity is `O(1)`. Some sorting algorithms might
require additional space.

#### Solution 3: Key Insights

- Extremely concise solution
- Works because the majority element must occupy the middle position after sorting
- Higher time complexity than other solutions due to sorting
```

## User ───

just give me the full file.

## Copilot ───

Let me provide you with the complete fixed version of the file:

[file:problems/majority_element.md](problems/majority_element.md)

```markdown
# Majority Element

## Problem Description

Given an array `nums` of size `n`, return the majority element.

The majority element is the element that appears more than `⌊n / 2⌋` times. You may assume that the majority element always exists in the array.

### Example 1:

```

Input: nums = [3,2,3]
Output: 3

```

### Example 2:

```

Input: nums = [2,2,1,1,1,2,2]
Output: 2

```

### Constraints:

- `n == nums.length`
- `1 <= n <= 5 * 10^4`
- `-10^9 <= nums[i] <= 10^9`

### Follow-up:
Could you solve the problem in linear time and in O(1) space?

## Solutions

### Solution 1: Hash Table

```python
def majorityElement(self, nums: List[int]) -> int:
    counter = {}

    for num in nums:
        counter[num] = counter.get(num, 0) + 1
    
    max = 0
    return_value = None
    for key, value in counter.items():
        if value > max:
            return_value, max = key, value
    return return_value
```

#### Solution 1: Approach

This solution uses a hash table (dictionary) to count the frequency of each element
in the array. We first iterate through the array to build a counter of each element.
Then, we find the element with the maximum count by iterating through the counter.

#### Solution 1: Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We traverse the array once to build the counter (`O(n)`) and then iterate through
the counter, which at most contains `n` distinct elements (`O(n)`). Therefore,
the total time complexity is `O(n)`.

##### Space Complexity: `O(n)`

In the worst case, if all elements are distinct, the counter would need to store
`n` key-value pairs.

#### Solution 1: Key Insights

- Simple and intuitive approach that works for all inputs
- Uses extra space to track frequency counts
- Requires two passes through the data (one for counting, one for finding maximum)

### Solution 2: Boyer-Moore Voting Algorithm

```python
def majorityElement(self, nums: List[int]) -> int:
    count = 0
    candidate = None
    
    for num in nums:
        if count == 0:
            candidate = num
        count += (1 if num == candidate else -1)
        
    return candidate
```

#### Solution 2: Approach

The Boyer-Moore Voting Algorithm is specifically designed for finding the majority
element. It works on the principle that if a majority element exists, it will
"survive" the pairwise cancellation of different elements. The algorithm maintains
a candidate element and a count. When the count reaches zero, we select a new
candidate.

#### Solution 2: Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We only need a single pass through the array.

##### Space Complexity: `O(1)`

We only use two variables (count and candidate) regardless of the input size.

#### Solution 2: Key Insights

- Satisfies the follow-up constraint of `O(1)` space complexity
- Works because the majority element appears more than `⌊n / 2⌋` times
- Elegant algorithm that doesn't require sorting or counting all elements

### Solution 3: Sorting

```python
def majorityElement(self, nums: List[int]) -> int:
    nums.sort()
    return nums[len(nums) // 2]
```

#### Solution 3: Approach

This solution sorts the array and returns the middle element. Since the majority
element appears more than `⌊n / 2⌋` times, it will always be at the middle position
after sorting.

#### Solution 3: Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Dominated by the sorting operation.

##### Space Complexity: `O(1)` or `O(n)`

If sorting in-place, the space complexity is `O(1)`. Some sorting algorithms might
require additional space.

#### Solution 3: Key Insights

- Extremely concise solution
- Works because the majority element must occupy the middle position after sorting
- Higher time complexity than other solutions due to sorting

### Comparison of Solutions

#### Time Complexity

- **Hash Table**: `O(n)` - Requires two passes through the data
- **Boyer-Moore**: `O(n)` - Single-pass algorithm
- **Sorting**: `O(n log n)` - Higher complexity due to sorting

#### Space Complexity

- **Hash Table**: `O(n)` - Requires space for frequency counter
- **Boyer-Moore**: `O(1)` - Constant extra space
- **Sorting**: `O(1)` if using in-place sorting, otherwise `O(n)`

#### Trade-offs

- The hash table solution is intuitive but uses extra space
- The Boyer-Moore algorithm is the most efficient, using linear time and constant space
- The sorting approach is concise but has higher time complexity

#### When to Use Each

- **Hash Table**: When code readability is prioritized over space efficiency
- **Boyer-Moore**: When optimal space and time complexity are required (ideal for large inputs)
- **Sorting**: When simplicity of implementation is the highest priority

#### Optimization Notes

- The Boyer-Moore algorithm is particularly elegant for this problem because it leverages the specific constraint that the majority element appears more than `⌊n / 2⌋` times
- For problems where a majority element isn't guaranteed to exist, the hash table approach would be more appropriate
